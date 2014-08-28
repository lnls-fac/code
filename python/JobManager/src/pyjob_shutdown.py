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
    parser.add_option('--sure', dest='sure',action='store_true',
                      help="Option to bypass the 'Are You Sure' question",
                      default=False)
    parser.set_description(description='When this command is called it shuts'
                           ' down the server')
    
    (opts, _) = parser.parse_args()
    
    if not opts.sure:
        Noyes = input('ARE YOU SURE you really want to'
                      ' shutdown the server [NO/yes]: ')
        if not Noyes or not 'yes'.startswith(Noyes.lower()):
            print('Wise decision! you did not shutdown the server.')
            return
        print('Ok, then...')
    
    # Load execution script
    handle_request('SHUTDOWN',  wait_for_reply=False)
    print('The server was shutdown!')
    
    
    
main()
