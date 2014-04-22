#!/usr/bin/python

import multiprocessing
import psutil
import socket
import sys
import pytask

class LocalMachine:
    def __init__(self):
        self.ip = socket.gethostbyname(socket.gethostname())
        self.cpu_count = multiprocessing.cpu_count()
    @staticmethod
    def get_pid_list():
        return psutil.get_pid_list()
    @staticmethod
    def get_pid_exists(pid):
        return psutil.pid_exists(pid = pid)
    @staticmethod 
    def kill_pid(pid):
        p = psutil.Process(pid)
        p.kill()

def cmd_get_ip(local_machine):
    print(local_machine.ip)
    
def cmd_get_cpu_count(local_machine):
    print(local_machine.cpu_count)
    
def cmd_get_pid_list(local_machine):
    pids = local_machine.get_pid_list()
    for pid in pids:
        print(pid)
        
def cmd_get_cmd_list(local_machine):
   for cmd in cmds:
       print(cmd)
       
def cmd_kill_pid(local_machine, pid): 
    try:
        local_machine.kill_pid(pid)
    except:
        print('error: could not kill process')
       
def cmd_get_task_pid_list(local_machine):
    pids = local_machine.get_pid_list()
    for pid in pids:
        p = psutil.Process(pid)
        if len(p.cmdline)>1:
            cmd = p.cmdline
            if pytask.task_label in cmd[1]:
                print(str(pid).rstrip())
    
 
''' command list of module '''   
cmds = {
        'get_cmd_list':cmd_get_cmd_list,
        'get_ip':cmd_get_ip,
        'get_cpu_count':cmd_get_cpu_count,
        'get_pid_list':cmd_get_pid_list,
        'get_task_pid_list':cmd_get_task_pid_list,
        'kill_pid':cmd_kill_pid,
       }


if __name__ == '__main__':

    if False:    
        local_machine = LocalMachine()
        cmds['get_task_pid_list'](local_machine)
    else:
        if len(sys.argv) < 2:
            print('error: invalid number of arguments')
        else:
            local_machine = LocalMachine()
            cmd = sys.argv[1]
            if cmd not in cmds:
                print('error: invalid command')
            elif cmd == 'kill_pid':
                cmds[sys.argv[1]](local_machine = local_machine, pid = int(sys.argv[2]))
            else:
                cmds[sys.argv[1]](local_machine = local_machine)
            
        
   