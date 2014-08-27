#!/usr/bin/env python3

import optparse
import calendar
import datetime
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
    parser.add_option('-c','--clients',dest='clients',type='str',
                      help="list of hosts to get the configs. "
                      "[format: client1,client2,...  default: 'all']")
    parser.add_option('-s', '--showCalendar',dest='sCal',action='store_true',
                      help="Show the calendar of each client", default=False)
         
    (opts, _) = parser.parse_args()
    
    
    clients = 'all'
    if opts.clients is not None:
        clients = opts.clients.split(",")
    
    ok, data = handle_request('GET_CONFIGS',clients)
    if ok:
        ConfigsReceived = data
    
    if clients != 'all':
        notmatched =  set(clients) - ConfigsReceived.keys()
        if notmatched:
            print("These clients: "+", ".join(notmatched) + "\n do not exist "
                  "in the server's list.")
            return
    
    if opts.sCal is not None:
        print('Calendar display not implemented yet')
    
    print('{0:15s} {1:^7s} {2:^12s} {3:^7s} {4:^7s} {5:^5s} '
          .format('hostname','state', 'numcpus' 'DefNumJobs', 'MoreJobs', 'Shut','Nice'))
    for k,v in ConfigsReceived.items():
        print('{0:15s} {1.active:^7} {1.numcpus:^5d} {1.defNumJobs:^12d} {1.MoreJobs:^7} '
              '{1.shutdown:^7} {1.niceness:^5d} '.format(k, v))
        
        
        
if __name__ == '__main__':
    main()

