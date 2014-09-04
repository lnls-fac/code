#!/usr/bin/env python3

import optparse
import calendar
import datetime
import calendar
import sys
import socket
import struct
import pickle
import Global
import pprint



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
    
    if opts.sCal:
        sortCal = lambda x:(getattr(calendar,x[0][0].upper()),x[0][1],x[0][2])
        sorTab = lambda x:getattr(calendar,x[0].upper())
        days = tuple(x for x in calendar.day_name)
        hours = tuple(range(24))
        minutes = tuple(range(60))
        for k, v in ConfigsReceived.items():
            np = ConfigsReceived[k].defNumJobs
            table = {x:dict() for x in calendar.day_name}
            conj = set()
            Cal = {(x,y,z): np for x in days for y in hours for z in minutes}
            Cal.update(ConfigsReceived[k].Calendar)
            previous = None
            lastday = calendar.day_name[0]
            for kl, vl in sorted(Cal.items(), key=sortCal):
                if vl != previous or kl[0] != lastday:
                    table[kl[0]].update({kl[1:]:vl})
                    conj.add(kl[1:])
                    previous = vl
                    lastday = kl[0]
            print(k)
            print(' '*9, calendar.weekheader(9))
            lasttime = dict() 
            for kl in sorted(conj, key=lambda x:x):
                nums = ''
                for day, dados in sorted(table.items(), key=sorTab):
                    vl = dados.get(kl)
                    if not vl:
                        vl = dados.get(lasttime[day])
                    else:
                        lasttime[day] = kl
                    
                    nums += '{:^10d}'.format(vl)
                print('{:^10s}{:s}'.format('{0:02d}:{1:02d}'.format(kl[0],
                                                                    kl[1]),
                                           nums))  
        return
    
    print('{:15s}{:^7s}{:^9s}{:^9s}{:^10s}{:^10s}{:^6s}'
          .format('hostname','state', 'numcpus','NumJobs',
                  'MoreJobs', 'Shutdown','Nice'))
    for k,v in ConfigsReceived.items():
        print('{0:15s}{1.active!s:^7s}{1.numcpus:^9d}{1.defNumJobs:^9d}'
              '{1.MoreJobs!s:^10}{1.shutdown!s:^10}{1.niceness:^6d}'
              .format(k,v))
        
        
        
if __name__ == '__main__':
    main()

