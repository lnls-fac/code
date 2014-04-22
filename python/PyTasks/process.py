import multiprocessing
import psutil
import paramiko
import socket


class Job:
    def __init__(self, 
                 start_timestamp  = None,
                 finish_timestamp = None,
                 local_machine    = None,
                 local_user       = None,
                 local_dir        = None,
                 remote_machine   = None,
                 remote_user      = None,
                 remote_dir       = None,
                 ):
        self.start_timestamp  = start_timestamp
        self.finish_timestamp = finis_timestamp
         
class LocalMachine:
    def __init__(self):
        self.ip = socket.gethostbyname(socket.gethostname())
        self.cpu_count = multiprocessing.cpu_count()
    @staticmethod
    def get_pids():
        return psutil.pids()
    @staticmethod
    def get_pid_exists(pid):
        return psutil.pid_exists(pid = pid)
        
class TaskServer:
    
    def __init__(self):
        self.cpu_count = multiprocessing.cpu_count()
        self.pids = psutil.get_pid_list()
        self.task = psutil.Process(self.pids[10])
     
   

lm = LocalMachine()
        
paramiko.util.log_to_file('ssh.log') # sets up logging

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('10.0.21.42', username='ximenes', password='XamddamX9')
#ssh.connect('127.0.0.1', username='ximenes', password='XamddamX9')
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("ls")
lines = ssh_stdout.readlines()
exit_status = ssh_stdout.channel.recv_exit_status()
ssh.close()


ts  = TaskServer()
print('ok')