#!/usr/bin/env python3

import optparse
import sys
import socket
import struct
import pickle
import Global

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

    parser = optparse.OptionParser()
    parser.add_option('-s','--status',dest='status',type='str',
                      help=("Select the jobs to show by their status. "
                            "[format: status1,status2,...  default: 'all']"))
    parser.add_option('-u','--user',dest='user',type='str',
                      help=("Select the jobs to show by their user. "
                            "[format: user1,user2,...  default: 'all']"))
    parser.add_option('-d','--description',dest='descr',type='str',
                      help="Select the jobs to show by a segment of their"
                      "description.")
    parser.set_description(description='This command lists the jobs in the '
                           ' queue.')
    
    (opts, _) = parser.parse_args()
    
    ok, Queue = handle_request('STATUS_QUEUE')
    if not ok:
        print("I don't know what happened, but the server did not respond"
              "as expected. maybe its a bug")
        return
    
    
    if opts.status is not None:
        status = set(opts.status.split(','))
        if not len(status - STATUS.keys()):
            print('Wrong status specification. Possible values are:\n'
                  ' '.join(list(k for k,v in sorted(STATUS.items(),
                                                    key= lambda x: x[1]))))
        Queue = Queue.SelAttrVal(attr='status_key',value=status)
        
    if opts.user is not None:
        user = set(opts.user.split(','))
        Queue = Queue.SelAttrVal(attr='user',value=user)
    
    if opts.descr is not None:
        Queue = Queue.SelAttrVal(attr='description',value=opts.descr)
    
    print('{:8s}{:^5s}{:^8s}{:^10s}{:^20s}{:^16s}{:^16s}{:^16s}'
      .format('Job ID','Prior', 'Status','User',
              'Description', 'Host Owner','Host Running','Possible Hosts'))
    for k,v in Queue.items():
        print('{0:^8}{1.priority:^5d}{1.status_key:^8s}{1.user:^10s}'
              '{1.description:20s}{1.hostname:^16s}{2:^16s}'
              .format(k, v, v.runninghost or 'None'), v.possiblehosts)

    
    
main()