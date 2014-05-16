import remote_machine
import getpass
import socket

default_machines = (
            ('lnls-fac-hpc1',   '10.2.105.176', 16), # bongers1
            ('lnls-fac-hpc2',   '10.2.105.178', 12), # bongers2
            ('lnls82-linux' ,   '10.0.21.42',   24), # fac-workstation
            ('lnls212-linux',   '10.0.21.100',   4), # natalia
            ('lnls209-linux',   '10.0.21.160',   4), # liu
            ('lnls208-linux',   '10.0.21.71',    8), # ximenes
            ('lnls210-linux',   '10.0.21.122',   8), # fernando
            
            #('lnls155-virtual', '10.0.21.144'),  # ricardo-virtual
            )


def get_running_pytasks_pid_list(ip_address, username, timeout = 5):
    rm = remote_machine.RemoteMachine(ip_address = ip_address, username = username, timeout = timeout)
    return rm.exec_command('local_machine.py get_pytask_pid_list')
    
    
def print_available_hosts(machines = None):
    
    if machines == None:
        machines = inquire_cpu_count()
    
    for host in machines:
        print('{0:16s} {1:15s} {2:12s} {3:03d} {4:03d}'.format(host[0], host[1], host[3], host[2], host[4]))
        
def inquire_cpu_count(machines = None):
    
    rm = None
    if machines == None:
        machines = default_machines
    new_machines = []
    for host in machines:
        if len(host) < 3:
            try:
                rm = remote_machine.RemoteMachine(ip_address = host[1], username = host[3], timeout = 5)
                result, exit_status = rm.exec_command('local_machine.py get_cpu_count')
                if (exit_status == 0) and ('error' not in result[0]):
                    new_machines.append((host[0], host[1], host[2], int(result[0])))
                else:
                    continue
            except socket.error:
                continue
        if len(host) < 4:
            host = (host[0],host[1],host[2],getpass.getuser())
        if len(host) < 5:
            try:
                if rm == None:
                    rm = remote_machine.RemoteMachine(ip_address = host[1], username = host[3], timeout = 5)
                result, exit_status = rm.exec_command('local_machine.py get_pytask_pid_list')
                nr_jobs = len(result)
                if (exit_status == 0) and (nr_jobs == 0 or ('error' not in result[0])):
                    new_machines.append((host[0], host[1], host[2], host[3], nr_jobs))
                else:
                    continue
            except socket.error:
                continue
                  
    return new_machines


print_available_hosts()

           

        
            
  
 







 


  
  
 

  
  
   

