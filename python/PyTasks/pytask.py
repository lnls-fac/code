#!/usr/bin/python

import signal
import sys
import os
import datetime
import uuid
import time


pytask_label = 'pytask.py'
default_pytask_dir = os.path.join(os.path.expanduser('~'), 'pytask_dir')

class LocalPyTask:
    
    def __init__(self, cmdline = None, remote_machine = None, remote_username = None, remote_dir = None):
        self.pid              = os.getpid()
        #self.id               = time.strftime('%Y-%m-%d-%H%M%S', time.localtime()) + '_' + str(uuid.uuid4())
        self.id               = time.strftime('%Y-%m-%d-%H%M%S', time.localtime()) + '_' + self.pid2str()
        self.remote_machine   = remote_machine
        self.remote_username  = remote_username
        self.remote_dir       = remote_dir
        self.cmdline          = cmdline
        self.local_dir        = os.path.join(default_pytask_dir, self.id)
        self.start_timestamp  = None,
        self.finish_timestamp = None,
        for sig in (signal.SIGABRT, signal.SIGTERM):
            signal.signal(sig, self.abort)
        if not os.path.exists(self.local_dir):
            os.makedirs(self.local_dir)
        self.fp = open(os.path.join(self.local_dir, 'pytask_status.txt'), 'w', 0)
        self.run()
            
    def pid2str(self):
        return '{0:08d}'.format(self.pid)
    
    def execute_task(self):
        self.fp.write(str(datetime.datetime.now()) + ': running...\n')
        time.sleep(60)
        #if self.cmdline is None:
        #    while True:
        #        pass
        
    def get_input_data(self):
        
        if self.remote_dir is None or self.remote_machine is None:
            return None
        self.fp.write(str(datetime.datetime.now()) + ': getting input data from ' + self.remote_machine + ' at ' + self.remote_dir + '...\n')
        cmd = 'scp -pr ' + self.remote_username + '@' + self.remote_machine + ':' + self.remote_dir + '/.' + ' ' + self.local_dir + '/'
        status = os.system(cmd)
        self.fp.write(str(datetime.datetime.now()) + ': input data received with status = ' + str(status) + '.\n')
        
        
    
    def send_results_back(self):
        pass
    
    def run(self):
        self.start_timestamp  = str(datetime.datetime.now())
        self.fp.write(self.start_timestamp + ': task with pid = ' + str(self.pid) + ' started.\n')
        self.get_input_data()
        self.execute_task()
        self.finish_timestamp = str(datetime.datetime.now())
        self.fp.write(self.finish_timestamp + ': finished.\n')
        self.fp.close()
        self.send_results_back()
        
    def abort(signal, frame):
        self.finish_timestamp = str(datetime.datetime.now())
        write(self.fp, self.finish_timestamp + ': aborted.\n')
        self.fp.close()
        self.send_results_back()
        sys.exit(0)




if __name__ == '__main__':
    lt = LocalPyTask(remote_machine = '10.0.21.42', remote_username = 'ximenes', remote_dir = '~/rodar_tracy')