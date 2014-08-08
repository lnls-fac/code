#!/usr/bin/python

import paramiko
import socket
import os
import sys

class RemoteMachine:
    
    def __init__(self, ip_address, username, password = None, fname = '~/.ssh/id_rsa', timeout = None):
        
        self.ip_address = ip_address
        self.username   = username
        self.password   = password
        self.fname      = fname
        self.timeout    = timeout

        paramiko.util.log_to_file('ssh.log') # sets up logging        
        self.ssh = paramiko.SSHClient() 
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())       
        
        privatekeyfile = os.path.expanduser(self.fname)
        mykey = paramiko.RSAKey.from_private_key_file(privatekeyfile)
        self.ssh.connect(self.ip_address, username = self.username, pkey = mykey, timeout = self.timeout)
        
    def exec_command(self, cmd):
        
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(cmd)
        result = ssh_stdout.readlines()
        for i in range(len(result)):
            result[i] = result[i].rstrip()
        exit_status = ssh_stdout.channel.recv_exit_status()
        #ssh.close()
        return result, exit_status
    
    def exec_command_in_background(self, cmd):
        
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(cmd + ' &')
        exit_status = ssh_stdout.channel.recv_exit_status()
        return exit_status
    
    
def cmd_get_cmd_list():
   for cmd in cmds:
       print(cmd) 

def cmd_get_cpu_count(remote_machine):

    result, exit_status = remote_machine.exec_command('local_machine.py get_cpu_count')
    for r in result:
        print(r)

def cmd_get_pytask_pid_list(remote_machine):

    result, exit_status = remote_machine.exec_command('local_machine.py get_pytask_pid_list')
    for r in result:
        print(r)
        
def cmd_kill_pid(remote_machine, pid):
    result, exit_status = remote_machine.exec_command('local_machine.py kill_pid ' + str(pid))
    for line in result:
        print(line)

    
    
''' command list of module '''   
cmds = {
        'get_cpu_count':cmd_get_cpu_count,
        'get_pytask_pid_list':cmd_get_pytask_pid_list,
        'get_cmd_list':cmd_get_cmd_list,
        'kill_pid':cmd_kill_pid,
       }

if __name__ == '__main__':
    
    if len(sys.argv) < 4:
            print('error: invalid number of arguments')
    else:
        ip_address, username, timeout, fname = sys.argv[1], sys.argv[2], sys.argv[3], '~/.ssh/id_rsa'
        rm = RemoteMachine(ip_address = ip_address, username = username, fname = fname, timeout = timeout)
        if sys.argv[4] == 'get_cmd_list':
            cmd_get_cmd_list()
        elif sys.argv[4] == 'get_pytask_pid_list':    
            cmd_get_task_pid_list(rm)
        elif sys.argv[4] == 'kill_pid':
            pid = sys.argv[5]
            cmd_kill_pid(rm, pid)
        elif sys.argv[4] == 'get_cpu_count':
            cmd_get_cpu_count(rm)
        else:
            print('error: invalid command')
                
                   
