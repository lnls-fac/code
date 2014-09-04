#!/usr/bin/env python3

import sys
import subprocess
import os
import datetime
import calendar
import time
import signal
import psutil
import shutil
import socket
import struct
import pickle
import Global

TEMPFOLDER    = os.path.join(os.path.split(
                             os.path.split(Global.__file__)[0])[0],
                             '.TempFolders')
FOLDERFORMAT  = 'jobid-{0:08d}'
JOBFILE       = 'pid-{0:d}'
JOBDONE       = 'done'
SUBMITSCR= ( 
'''#!/bin/bash
./{0} > {1:08d}.out 2> {1:08d}.err
touch {2}''')
SUBMITSCRNAME = 'run_{0:08d}'

Address     = Global.Address
VERSION     = Global.VERSION
MAX_BLOCK_LEN = Global.MAX_BLOCK_LEN
PICKLE_PROTOCOL = Global.PICKLE_PROTOCOL
WAIT_TIME = Global.WAIT_TIME
SET_STRUCT_PARAM = Global.SET_STRUCT_PARAM

class SocketManager:
    def __init__(self, address):
        self.address = address
    
    def __enter__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(Address)
        return self.sock
    
    def __exit__(self, *ignore):
        self.sock.close()
    

def handle_request(*items, wait_for_reply=True):
    InfoStruct = struct.Struct(SET_STRUCT_PARAM)
    data = pickle.dumps(items,PICKLE_PROTOCOL)
    try:
        with SocketManager(tuple(Address)) as sock:
            sock.sendall(InfoStruct.pack(len(data), VERSION))
            sock.sendall(data)
            if not wait_for_reply:
                return
            size_data = sock.recv(InfoStruct.size)
            size = InfoStruct.unpack(size_data)[0]
            result = bytearray()
            while True:
                data = sock.recv(MAX_BLOCK_LEN)
                if not data:
                    break
                result.extend(data)
                if len(result) >= size:
                    break
            return pickle.loads(result)
    except socket.error as err:
        print("{0}: is the pyjob_server running?".format(err))
        sys.exit(1)
        


def load_jobs_from_last_run():
    ''' Check if there are jobs running from last call of the script.
    Change the status to ended if the job terminated in between calls
    Change the status to terminated if it was interrupted
    Set status to paused if the job is Stopped in the os'''
    
    if not os.path.isdir(TEMPFOLDER):
        os.mkdir(path=TEMPFOLDER)
    for folder in os.listdir(path=TEMPFOLDER):
        if os.path.isdir(os.path.join(TEMPFOLDER,folder)):
            jobid = int(folder.split('-')[1])
            for file in os.listdir(path='/'.join([TEMPFOLDER,folder])):
                if file.startswith( JOBFILE[:4]):
                    pid = int(file.split('-')[1])
                    break
            fh = None
            try:
                fh = open('/'.join([TEMPFOLDER,folder,JOBFILE.format(pid)]))
                file_data = fh.read()
            finally:
                if fh is not None:
                    fh.close()
            
            proc = Global.MimicsPsutilPopen(pid = pid)
            job = eval(file_data)
            state = proc.poll()
            folder = FOLDERFORMAT.format(jobid)
            if (state is not None or
                proc.name not in '/'.join([folder, SUBMITSCRNAME.format(jobid)])):
                if os.path.isfile('/'.join([TEMPFOLDER,folder,JOBDONE])):
                    job.status_key = 'e'
                else:
                    job.status_key = 't'
            else:
                if proc.status == 'stopped':
                    job.status_key = 'p'
            jobid2proc.update({jobid : proc})
            MyQueue.update({jobid : job})

def shutdown():
    ok = handle_request('GOODBYE')
    if ok:
        sys.exit()
    sys.exit(1)
    
def check_running_jobs():
    count = 0
    for jobid, proc in jobid2proc.items():
        state = proc.poll()
        folder = FOLDERFORMAT.format(jobid)
        if state is not None:
            if os.path.isfile('/'.join([TEMPFOLDER,folder,JOBDONE])):
                MyQueue[jobid].status_key = 'e'
            else:
                if MyQueue[jobid].status_key != 'q':
                    MyQueue[jobid].status_key = 't'
        else:
            if proc.status in {'running','sleeping'}:
                count +=1
    return count

def deal_with_finished_jobs():
    for k, v in MyQueue.items():
        if v.status_key in {'e', 't', 'q'}:
            folder = '/'.join([TEMPFOLDER, FOLDERFORMAT.format(k)])
            jobf= JOBFILE.format(jobid2proc[k].pid)
            files = os.listdir(path=folder)
            for file in set(files) - (v.input_files.keys() |
                                       set([jobf,JOBDONE])):
                data = Global.load_file(os.path.join(folder,file))
                v.output_files.update({file: data})
            MyQueue.update({k:v})

def deal_with_configs():
    agora = datetime.datetime.now()
    allowed = MyConfigs.Calendar.get((calendar.day_name[agora.weekday()],
                                   agora.hour,
                                   agora.minute),
                                  MyConfigs.defNumJobs)
    
    for proc in jobid2proc.values():
        if not proc.poll():
            if proc.get_nice() != MyConfigs.niceness:
                proc.set_nice(MyConfigs.niceness)
            
    return allowed

def submit_jobs(NewQueue):
    for k, v in NewQueue.items():
        #create temporary directory
        tempdir = '/'.join([TEMPFOLDER,FOLDERFORMAT.format(k)])
        os.mkdir(tempdir)
        #create files
        Global.createfile(name ='/'.join([tempdir,SUBMITSCRNAME.format(k)]),
                          data =SUBMITSCR.format(v.execution_script_name, k,
                                                 JOBDONE),
                          stats= Global.MyStats(st_mode=0o774))
        for name, info in v.execution_script.items():
            Global.createfile(name = '/'.join([tempdir,name]),
                              data = info[1], stats = info[0])
        for name, info in v.input_files.items():
            Global.createfile(name='/'.join([tempdir, name]),
                              data = info[1], stats = info[0])
        for name, info in v.output_files.items():
            Global.createfile(name='/'.join([tempdir, name]),
                              data = info[1], stats = info[0])
        #submit job
        proc = psutil.Popen('/'.join([tempdir, SUBMITSCRNAME.format(k)]),
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                            start_new_session=True,
                            cwd = tempdir)
        #update queues
        v.status_key = 'r'
        proc.set_nice(MyConfigs.niceness)
        MyQueue.update({k:v})
        jobid2proc.update({k:proc})
        #create job file for, if necessary, later loading
        Global.createfile(name = '/'.join([tempdir,JOBFILE.format(proc.pid)]),
                          data = repr(v))

def stop_jobs(jobs2Stop = 0):
    RunningQueue = MyQueue.SelAttrVal(attr='status_key', value={'r'})
    for _ in range(jobs2Stop):
        k, v = RunningQueue.poplast()
        os.killpg(jobid2proc[k].pid,signal.SIGSTOP)
        v.status_key = 'p'
        MyQueue.update({k:v})

def continue_stopped_jobs(jobs2Continue = 1):
    StoppedQueue = MyQueue.SelAttrVal(attr='status_key', value={'p'})
    if not len(StoppedQueue): return 0
    for i in range(jobs2Continue):
        k, v = StoppedQueue.popfirst()
        os.killpg(jobid2proc[k].pid,signal.SIGCONT)
        v.status_key = 'r'
        MyQueue.update({k:v})
        if not len(StoppedQueue): break
    return i + 1

def deal_with_results(ResQueue):
    for v in ResQueue.values():
        for name, content in v.output_files.items():
            Global.createfile(name = os.path.join(v.working_dir,name),
                              data = content[1], stats = content[0])

def deal_with_signals(Jobs2Sign):
    for k, v in Jobs2Sign.items():
        if v.status_key == 'pu':
            os.killpg(jobid2proc[k].pid, signal.SIGSTOP)
        elif v.status_key == 'tu':
            os.killpg(jobid2proc[k].pid, signal.SIGTERM)
            os.killpg(jobid2proc[k].pid, signal.SIGCONT)
            v.status_key = 't'
        elif v.status_key == 'ru':
            os.killpg(jobid2proc[k].pid, signal.SIGCONT)
            v.status_key = 'r'
        elif v.status_key == 'qu':
            os.killpg(jobid2proc[k].pid, signal.SIGTERM)
            os.killpg(jobid2proc[k].pid, signal.SIGCONT)
            v.runninghost = None
            v.status_key = 'q'
        elif v.status_key == 'ch':
            v.status_key = MyQueue[k].status_key
        MyQueue.update({k:v})
           


MyQueue = Global.JobQueue()
jobid2proc = dict()
MyConfigs = Global.Configs()

def main():
       
    load_jobs_from_last_run()
    deal_with_finished_jobs()
    
    global MyConfigs
    ok, data = handle_request('GIME_CONFIGS', MyConfigs)
    if ok:
        MyConfigs = data

    
    while True:
        num_running = check_running_jobs()
        deal_with_finished_jobs()
        num_allowed = deal_with_configs()
        jobs2Continue = num_allowed - num_running
        if jobs2Continue > 0:
            continued = continue_stopped_jobs(jobs2Continue)
            jobs2Submit = jobs2Continue - continued
            if jobs2Submit > 0 and MyConfigs.MoreJobs:
                ok, NewQueue = handle_request('GIME_JOBS',jobs2Submit)                 
                if ok:
                    submit_jobs(NewQueue)
        elif jobs2Continue < 0 :
            jobs2Stop = -jobs2Continue
            stop_jobs(jobs2Stop)
        
        ok, keys2remove, Jobs2Sign = handle_request('UPDATE_JOBS', MyQueue)
        if ok:
            for key in keys2remove:
                jobid2proc.pop(key)
                MyQueue.pop(key)
                shutil.rmtree('/'.join([TEMPFOLDER,FOLDERFORMAT.format(key)]))
            if Jobs2Sign:
                deal_with_signals(Jobs2Sign)
            
        ok, ResQueue = handle_request('GIME_RESULTS')
        if ok:
            deal_with_results(ResQueue)

        time.sleep(WAIT_TIME)

        ok, data = handle_request('GIME_CONFIGS',MyConfigs)
        if ok:
            MyConfigs = data
        
        if MyConfigs.shutdown:
            shutdown()
        
if __name__ == '__main__':
    proclist = psutil.get_process_list()
    mod_name = os.path.split(__file__)[1]
    mypid = os.getpid()
    for proc in proclist:
        for cmdline in proc.cmdline:
            if mod_name in cmdline and proc.pid != mypid:
                print('There is already one instance of {0}'
                      ' running on this computer: exiting'.format(mod_name))
                sys.exit(1)
    main()