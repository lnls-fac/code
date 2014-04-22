import paramiko
import socket
import os


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
        exit_status = ssh_stdout.channel.recv_exit_status()
        #ssh.close()
        return result, exit_status
    
    
rm = RemoteMachine(ip_address = '10.0.21.42', username = 'ximenes', timeout = 1)
result, exit_status = rm.exec_command('local_machine get_task_pid_list')
r2 = rm.exec_command('ls')
print(r1)