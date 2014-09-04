#!/usr/bin/env python3

import optparse
import sys
import os
import socket
import struct
import pickle
import Global
from builtins import isinstance


Address = Global.Address
VERSION = Global.VERSION
MAX_BLOCK_LEN = Global.MAX_BLOCK_LEN
PICKLE_PROTOCOL = Global.PICKLE_PROTOCOL
SET_STRUCT_PARAM = Global.SET_STRUCT_PARAM
STATUS = Global.STATUS

class SocketManager:
    def __init__(self, address):
        self.address = address
    
    def __enter__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.address)
        return self.sock
    
    def __exit__(self, *ignore):
        self.sock.close()
    

def handle_request(*items, wait_for_reply=True):
    InfoStruct = struct.Struct(SET_STRUCT_PARAM)
    data = pickle.dumps(items,PICKLE_PROTOCOL)
    try:
        with SocketManager(Address) as sock:
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

def main():
    
    # configuration of the parser for the arguments
    parser = optparse.OptionParser()
    group = optparse.OptionGroup(parser, "Job Selection Options")
    group.add_option('-J','--jobs',dest='jobs',type='str',
                     help="list of jobs to send the signal [format:"
                     "job1,job2,...")
    group.add_option('-S','--status',dest='status',type='str',
                     help="Select the jobs by their status. "
                     "[format: status1,status2,...  default: 'all']")
    group.add_option('-U','--user',dest='user',type='str',
                     help="Select the jobs by their user. "
                     "[format: user1,user2,...  default: 'all']")
    group.add_option('-D','--description',dest='descr',type='str',
                     help="Select the jobs by a segment of their description.")
    parser.add_option_group(group)
    group = optparse.OptionGroup(parser, "Signals Options")
    group.add_option('-s', '--signal', dest='signal', type='str',
                     help="Send signal to jobs. Options are: kill, pause or " 
                     "continue")
    group.add_option('-p', '--priority', dest='priority', type='int',
                     help="Change priority of jobs. Must be an integer")
    group.add_option('-H', '--possibleHosts', dest='hosts', type='str',
                     help="Change the list of possible hosts to run the"
                     "jobs [format: append=host1,host2,... or set=host1,host2"
                     ",...")
    group.add_option('-q', '--queue', dest='queue', action='store_true',
                      help="This option brings back to the queue a job"
                      "which was already sent to a client. If it is running"
                      " the outputs generated so far will be loaded",
                      default=False)
    parser.add_option_group(group)
    
    parser.set_description(description='This command send signals to specific '
                           'jobs.')
    
    (opts, _) = parser.parse_args()
    
    if not any((opts.jobs,opts.status,opts.user,opts.descr)):
        print('At least one Job Selection Option must be given')
        return
    
    if opts.jobs and any((opts.status,opts.user,opts.descr)):
        print('When the option -J is given the other Job Selection Options'
              'can not be used.')
        return
    
    ok, Queue = handle_request('STATUS_QUEUE')
    
    if not ok:
        print("I don't know what happened, but the server did not respond"
              "as expected. maybe its a bug")
        return
   
    if opts.jobs is not None:
        try:
            jobs = set([ int(x) for x in opts.jobs.split(',')])
        except ValueError as err:
            print(err)
            return
        nonexistent_jobs = list(jobs - set(Queue.keys()))
        if nonexistent_jobs:
            print('These jobs do not exist:', ' '.join(nonexistent_jobs))
            return
        Queue = Global.JobQueue({k:v for k,v in Queue.items() if k in jobs})
    
    if opts.status is not None:
        status = set(opts.status.split(','))
        if len(status - STATUS.keys()):
            print('Wrong status specification. Possible values are:',
                  ' '.join(list(k for k,v in sorted(STATUS.items(),
                                                    key= lambda x: x[1]))))
            return
        Queue = Queue.SelAttrVal(attr='status_key',value=status)
        
    if opts.user is not None:
        user = set(opts.user.split(','))
        Queue = Queue.SelAttrVal(attr='user',value=user)
    
    if opts.descr is not None:
        Queue = Queue.SelAttrVal(attr='description',value=opts.descr)

    if Queue.SelAttrVal(attr='status_key', value={'t','e','tu'}):
        print("You are trying to change a job which is finished: Operation"
              " not allowed.")
        return

    signals = dict({'kill':'tu','pause':'pu','continue':'ru'})
    if opts.signal is not None:
        if opts.signal.lower() not in signals.keys():
            print('Signal not supported')
            return
        for k in Queue:
            Queue[k].status_key = signals[opts.signal.lower()]
    
    if opts.hosts is not None:
        action = opts.hosts.split('=')
        if len(action) != 2: 
            print('Wrong -H assignment.')
            return
        hosts = set(action[1].split(','))
        for k,v in Queue.items():
            if len(hosts) == 1 and not hosts.symmetric_difference({'all'}):
                v.possiblehosts = 'all';
                v.status_key = 'ch'
                continue
            if 'append'.startswith(action[0].lower()):
                if v.possiblehosts == 'all':
                    continue
                v.possiblehosts += hosts
                v.status_key = 'ch'
            elif 'set'.startswith(action[0].lower()):
                v.possiblehosts = hosts
                v.status_key = 'ch'
            else:
                print('Wrong -H assignment.')
                return
            Queue.update({k:v})
    
    if opts.priority is not None:
        for k,v in Queue.items():
            v.priority = opts.priority
            v.status_key = 'ch'
            Queue.update({k:v})
    
    if opts.queue:
        for k,v in Queue:
            if v.status_key != 'q':
                Queue[k].status_key = 'qu'
            else:
                print('You are trying to send a job which already is in q'
                      ' state to the q state. Operation not allowed.')
                return
        
    ok, data1, data2 = handle_request('CHANGE_JOBS_REQUEST',Queue)

    if ok:
        pr1 = [str(x) for x in data1]
        pr2 = [str(x) for x in data2]
        print('These jobs were successfully changed:', ' '.join(pr1))
        print('These jobs were scheduled to change: ', ' '.join(pr2))
        left = [str(x) for x in set(Queue.keys()) - (data1 | data2)]
        if left:
            print('These jobs could not be changed :', ' '.join(left))

    
if __name__ == '__main__':
    main()
