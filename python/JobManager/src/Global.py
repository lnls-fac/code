#!/usr/bin/env python3

import socket
import os
import signal
import getpass
import pwd
import psutil
import datetime

#Address = ('fernando-linux', 8804)
Address = ('lnls210-linux', 8804)
VERSION = '0.0.0'.encode('utf-8')
MAX_BLOCK_LEN = 1024*4
PICKLE_PROTOCOL = 3
SET_STRUCT_PARAM = "!I 5s"
STATUS = dict(q=1, # queued
                       r=4, # running
                       p=2, # paused
                       w=3, # waiting
                       t=5, # terminated
                       e=6, # ended
                       s=7) # sent

class JobErr(Exception): pass
class Jobs:
   
    def __init__(self,
                 description = 'generic job',
                 user = getpass.getuser(),
                 working_dir = None,
                 creation_date = None,
                 status_key = None,
                 hostname = None,
                 runninghost = None,
                 priority = 0,
                 input_files = dict(),#keys are file names and values the data
                 execution_script = dict(),#idem to input_files
                 output_files = dict()#keys -> names values are tuples of data
                 ):                   # and creation/modification times
        
        self.description = description
       
        try:
            pwd.getpwnam(user)
        except KeyError:
            raise JobErr('Specified user does not exist')
        else:
            self.user = user
        
        self.working_dir = os.path.abspath(working_dir or os.getcwd())
        
        self.creation_date = creation_date or datetime.datetime.now()
        self.status_key = status_key or 'q'
        self.hostname = hostname or socket.gethostname()
        self.priority = priority
        self.runninghost = runninghost
        
        # Load input files
        self.input_files = input_files
        #Load Execution Script
        self.execution_script = execution_script
        # Load output files
        self.output_files = output_files
    

    @property
    def input_file_names(self): return list(self.input_files.keys())
    
    @property
    def output_file_names(self): return list(self.output_files.keys())
    
    @property
    def execution_script_name(self): return list(self.execution_script.keys())[0]
        
    
    def __lt__(self,other):
        if not isinstance(other, Jobs):
            return NotImplemented
        if self.status_key != other.status_key:
            if (STATUS[self.status_key] < STATUS[other.status_key]):
                return True
            return False
        else:
            if self.priority > other.priority:
                return True
            elif self.priority == other.priority:
                if self.creation_date < other.creation_date:
                    return True
            return False

    def __eq__(self,other):
        if not isinstance(other, Jobs):
            return NotImplemented
        elif not (self < other or other < self):
            return True
        else:
            return False
    
    def __le__(self,other):
        return True if self == other or self < other else False
    
    def __repr__(self):
        return representational_form(self)
   
    def __str__(self):
        return ("description = {0.description},\nuser = {0.user},\n"
                "working_dir = {0.working_dir},\n"
                "creation_date = {0.creation_date},\n"
                "status_key = {0.status_key},\nhostname = {0.hostname},\n"
                "priority = {0.priority},\n"
                "input_file_names = {0.input_file_names},\n"
                "execution_script_name = {0.execution_script_name},\n"
                "output_file_names = {0.output_file_names}"
                .format(self))
    
    def __hash__(self):
        return hash(id(self))

keyQueue= lambda x: x[1]
class JobQueue(dict):
    
    def __repr__(self):
        return ("{0}.{1}(".format(self.__class__.__module__,
                                  self.__class__.__name__)
                + super().__repr__() + ")")
    
    def poplast(self):
        try:
            key = list(self.items())[-1][0]
        except IndexError:
            raise KeyError("poplast(): dictionary is empty")
        return key, self.pop(key)

    def popfirst(self):
        try:
            key = list(self.items())[0][0]
        except IndexError:
            raise KeyError("popfirst(): dictionary is empty")
        return key, self.pop(key)
    
    def values(self):
        for _, value in sorted(super().items(),key=keyQueue):
            yield value
        if len(self) == 0: super().values()
    
    def items(self):
        for key, value in sorted(super().items(),key=keyQueue):
            yield key, value
        if len(self) == 0: super().items()
    
    def __iter__(self):
        for key, _ in sorted(super().items(),key=keyQueue):
            yield key
        if len(self) == 0: super().keys()
    
    keys = __iter__
            
    def copy(self):
        return JobQueue(self)
    
    __copy__ = copy
    
    def SelAttrVal(self,attr='status_key', value={'r'}):
        newqueue = JobQueue()
        if not isinstance(value, set): value = set(value)
        for k,v in self.items():
            if v.__getattribute__(attr) in value:
                newqueue.update({k:v})
        return newqueue
        
    
class Configs:
    def __init__(self, shutdown = False, MoreJobs = True, niceness=0,
                 defNumJobs = 0, Calendar = dict(), active = True):
        self.shutdown = shutdown
        self.MoreJobs = MoreJobs
        self.niceness = niceness
        self.defNumJobs = defNumJobs
        self.Calendar =  Calendar
        self.active = active
        
    def __repr__(self):
        return representational_form(self)

class MimicsPsutilPopen(psutil.Process):
    def __init__(self,pid=None):
        try:
            super().__init__(pid)
            self.__returncode = None
        except psutil._error.NoSuchProcess:
            self.__returncode = signal.SIGTERM

    @property
    def returncode(self):
        return self.__returncode
    
    def poll(self):
        if self.is_running() and self.status != 'zombie':
            self.__returncode = None
        else:
            self.__returncode = signal.SIGTERM
        return self.__returncode
    
    def send_signal(self, sign):
        super().send_signal(sign)
        self.__returncode = sign
    
    def kill(self):
        super().kill(signal.SIGKILL)
        self.__returncode = signal.SIGKILL
    
    def terminate(self):
        super().terminate()
        self.__returncode = signal.SIGTERM
     
class MyStats:
    def __init__(self, name=None, st_mode=0o664,
                 st_atime = None, st_mtime = None):
        if name is not None:
            file_stats = os.stat(name)
            self.st_mode = file_stats.st_mode
            self.st_atime = file_stats.st_atime
            self.st_mtime = file_stats.st_mtime
        else:
            self.st_mode = st_mode
            self.st_atime = st_atime
            self.st_mtime = st_mtime
            
    def __repr__(self):
        return representational_form(self)
        
        
def createfile(name= None, data=None, stats = MyStats(), owner = None):
    if not name:
        raise ValueError('Name not specified')
    try:
        with open(name,'w') as fh:
            fh.write(data or '')
    except (IOError, OSError) as err:
        print('Problem with output files:\n',err)
        return None
    mode = stats.st_mode
    os.chmod(name, mode)
    times = None
    if stats.st_atime or stats.st_mtime:
        atime = stats.st_atime
        mtime = stats.st_mtime
        times = (atime,mtime)
    os.utime(name, times=times)
    try:
        user = pwd.getpwnam(owner)
        os.chown(name, user.pw_uid, user.pw_gid)
    except (TypeError, KeyError):
        pass

def load_file(name, ignore=False):
    try:
        with open(name) as fh:
            file_data = fh.read()
    except (TypeError, IOError, OSError) as err:
        if not ignore:
            print('Problem with file {0}:\n'.format(name),err)
        return None
    file_stats = MyStats(name)
    return file_stats, file_data

def representational_form(ob):
    form ="{0}.{1}(" + ",  ".join(["{0} = {{2.{0}!r}}".format(x) 
                                   for x in sorted(ob.__dict__.keys())
                                   if not x.startswith("_")]) + ")"
    return form.format(ob.__class__.__module__, ob.__class__.__name__, ob)


if __name__ == '__main__':
    job = Jobs(priority=1)
    queuee = JobQueue()
    queuee.update({2:job})
    repr(queuee)
    


