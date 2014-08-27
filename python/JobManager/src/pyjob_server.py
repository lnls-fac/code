#!/usr/bin/env python3

#import remote_machine
import datetime
import socketserver
import struct
import threading
import gzip
import sys
import pickle
import os
import socket
import Global

Address = Global.Address
VERSION = Global.VERSION
MAX_BLOCK_LEN = Global.MAX_BLOCK_LEN
PICKLE_PROTOCOL = Global.PICKLE_PROTOCOL
WAIT_TIME = Global.WAIT_TIME
SET_STRUCT_PARAM = Global.SET_STRUCT_PARAM
STATUS = Global.STATUS
CONFIGFOLDER  = os.path.join(os.path.split(Global.__file__)[0],'.configs') #for now
IDGEN_FILENAME = 'last_id'
QUEUE_FILENAME = 'Queue'
CONFIGS_FILENAME = 'clients_configs'

class ManageJobsServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class GzipManager:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
    
    def __enter__(self):
        self.fh = gzip.open(self.filename, self.mode)
        return self.fh
        
    def __exit__(self, *ignore):
        self.fh.close()

class Finish(Exception): pass

class RequestHandler(socketserver.StreamRequestHandler):
    
    ConfigsLock = threading.Lock()
    QueueLock   = threading.Lock()
    CallLock    = threading.Lock()
    IdGenLock   = threading.Lock()
    
    Configs     = None
    IdGen       = None
    Queue       = None
    Call = dict( 
        GIME_JOBS=(
            lambda self, *args: self.send_job_from_queue(*args)),
        GIME_RESULTS=(
            lambda self, *args: self.send_results_to_host(*args)),
        NEW_JOB=(
            lambda self, *args: self.add_new_job_to_queue(*args)),
        UPDATE_JOBS=(
            lambda self, *args: self.update_jobs_in_queue(*args)),  
        STATUS_QUEUE=(
            lambda self, *args: self.print_queue_status(*args)),
        GIME_CONFIGS=(
            lambda self, *args: self.send_configs_to_client(*args)),  
        SET_CONFIGS=(
            lambda self, *args: self.set_configs_of_clients(*args)),
        GET_CONFIGS=(
            lambda self, *args: self.get_configs_of_clients(*args)),
        SHUTDOWN=(
            lambda self, *args: self.shutdown(*args)),
        GOODBYE=(
            lambda self, *args: self.client_shutdown(*args))
        )

    def handle(self):
        InfoStruct = struct.Struct(SET_STRUCT_PARAM)
        info = self.rfile.read(InfoStruct.size)
        size, version = InfoStruct.unpack(info)
        data = pickle.loads(self.rfile.read(size))
        if version != VERSION:
            reply = (False, 'client is incompatible')
        else:
            try:
                with self.CallLock:
                    function = self.Call[data[0]]
                reply = function(self, *data[1:])
            except Finish:
                return
        data = pickle.dumps(reply, PICKLE_PROTOCOL)
        self.wfile.write(InfoStruct.pack(len(data), VERSION))
        self.wfile.write(data)

    @classmethod
    def add_new_job_to_queue(cls, job):
        with cls.IdGenLock, cls.QueueLock:
            jobid = cls.IdGen
            cls.IdGen += 1 
            cls.Queue.update({jobid : job})
        return (True, jobid)
    
    def send_results_to_host(self):
        clientName = socket.gethostbyaddr(self.client_address[0])[0]
        if clientName == 'localhost':
            clientName = socket.gethostname()
        with self.QueueLock:
            ResQueue = self.Queue.SelAttrVal(attr='status_key',
                                             value={'e','t'})
        EnvQueue = ResQueue.SelAttrVal(attr='hostname',value={clientName})
        if EnvQueue: 
            with self.QueueLock:
                for k in EnvQueue.keys():
                    self.Queue.pop(k)
            return (True, EnvQueue)
        return (False, None)
    
    def send_configs_to_client(self, ItsConfigs):
        clientName = socket.gethostbyaddr(self.client_address[0])[0]
        if clientName == 'localhost':
            clientName = socket.gethostname()
        with self.ConfigsLock:
            if clientName in self.Configs.keys():
                self.Configs[clientName].numcpus = ItsConfigs.numcpus
                self.Configs[clientName].active = 'on'
                self.Configs[clientName].last_contact = datetime.datetime.now()
                return (True, self.Configs[clientName])
            
            self.Configs.update({clientName:ItsConfigs})
            self.Configs[clientName].active = True
            self.Configs[clientName].last_contact = datetime.datetime.now()
            return (False, True)
    
    
    def send_job_from_queue(self,jobs2send):
        QueuedJobs = Global.JobQueue()
        Jobs2Send = Global.JobQueue()
        with self.QueueLock:
            QueuedJobs.update(self.Queue.SelAttrVal(attr='status_key',
                                                    value={'q'}))
            if not len(QueuedJobs): return (False, None)
            for k,v in QueuedJobs.items():
                v.status_key = 's'
                v.runninghost = socket.gethostbyaddr(
                                                self.client_address[0])[0]
                if v.runninghost == 'localhost':
                    v.runninghost = socket.gethostname()
                Jobs2Send.update({k:v})
                self.Queue.update({k:v})
                if len(Jobs2Send) >= jobs2send: break
        return (True, Jobs2Send)
            
    def print_queue_status(self):
        return (True, self.Queue)
    
    def update_jobs_in_queue(self, ItsQueue):
        keys2remove = []
        with self.QueueLock:
            for k, v in ItsQueue.items():
                value = self.Queue.get(k)
                if value is not None:
                    self.Queue.update({k:v})
                else:
                    print('job {0:08d} exists in {1.runninghost}'
                          'but not in server: deleting!'.format(k,v))
                if v.status_key in {'e','t'}:
                    keys2remove.append(k)
        return (True, keys2remove)
    
    def get_configs_of_clients(self, clients):
        if clients == 'all':
            clients = tuple(self.Configs.keys())
            
        Configs2Send = {}        
        with self.ConfigsLock:
            for clientName in clients:
                if clientName in self.Configs.keys():
                    if (3*WAIT_TIME < datetime.datetime.now().timestamp() - 
                        self.Configs[clientName].last_contact.timestamp()
                        and self.Configs[clientName].active == 'on'):
                        self.Configs[clientName]. active = 'dead'
                    ClientConfigs = self.Configs[clientName]
                    Configs2Send.update({clientName: ClientConfigs})
            return (True, Configs2Send)

    def set_configs_of_clients(self, NewConfigs):
        clients = tuple(NewConfigs.keys() - self.Configs.keys())
        if clients:
            return (False, clients)
        with self.ConfigsLock: self.Configs.update(NewConfigs)
        return (True, None)
    
    def shutdown(self):
        self.server.shutdown()
        save()
        raise Finish()
    
    def client_shutdown(self):
        clientName = socket.gethostbyaddr(self.client_address[0])[0]
        if clientName == 'localhost':
            clientName = socket.gethostname()
        with self.ConfigsLock:
            self.Configs[clientName].active = 'off'
            self.Configs[clientName].shutdown = False
            self.Configs[clientName].MoreJobs = True
        return True
        

        
def load_existing_Queue():
    name   = os.path.join(CONFIGFOLDER,QUEUE_FILENAME)
    data = Global.load_file(name=name, ignore = True)
    if data and data[1]: return eval(data[1])
    return

def load_last_id():
    name   = os.path.join(CONFIGFOLDER,IDGEN_FILENAME)
    data = Global.load_file(name=name, ignore = True)
    if data and data[1]: return eval(data[1])
        
def load_existing_Configs():
    name   = os.path.join(CONFIGFOLDER,CONFIGS_FILENAME)
    data = Global.load_file(name=name, ignore = True)
    if data and data[1]: return eval(data[1])

def save():
    idgenname   = os.path.join(CONFIGFOLDER,IDGEN_FILENAME)
    queuename   = os.path.join(CONFIGFOLDER,QUEUE_FILENAME)
    configname = os.path.join(CONFIGFOLDER,CONFIGS_FILENAME)
    Global.createfile(name=idgenname, data=repr(RequestHandler.IdGen))
    Global.createfile(name=queuename, data=repr(RequestHandler.Queue))
    Global.createfile(name=configname, data=repr(RequestHandler.Configs))

def main():
    RequestHandler.Queue = load_existing_Queue() or Global.JobQueue()
    RequestHandler.IdGen = load_last_id() or int(1)
    RequestHandler.Configs = load_existing_Configs() or dict()
    server = None
    try:
        server = ManageJobsServer(("", Address[1]), RequestHandler)
        server.serve_forever()
    except Exception as err:
        print("ERROR", err)
    finally:
        if server is not None:
            server.shutdown()
            save()

if __name__ == '__main__':
    main()

    #fuser -Address[1]/tcp
  
   

