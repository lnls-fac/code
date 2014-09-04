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
                      help="list of hosts to set calendar. "
                      "[format: client1,client2,...  default: 'this']")
    parser.add_option('-n','--niceness',dest='niceness',type='int',
                      help="Niceness of the jobs submitted by the clients. "
                      "[default: 'current value']")
    parser.add_option('-s','--shutdown',dest='shut',type='string',
                      help="If true shutdown the clients. ")
    parser.add_option('-j','--MoreJobs',dest='More',type='string',
                      help="If false, the clients won't ask for new jobs.")
    parser.add_option('-d','--defnumproc',dest='defproc',type='int',
                      help="Default number of processes the clients can run."
                      "It means that for the set of (W,H,M) not specified "
                      "in the calendar this will be the number of jobs each"
                      " client will run. [default: current value]")
    group = optparse.OptionGroup(parser, "Calendar Options")
    group.add_option('--calendar',dest='calendar',type='str',
                      help="If this option is given, the calendar of the "
                      "clients will be set with the following options or "
                      "their default values. [Possible values: " 
                      "'append' and 'set'   default: 'append']")
    group.add_option('-W','--weekday',dest='week',type='str',
                      help=("list of week days to set the calendar. "
                      "[format: day1,day2,... default is the weekday of today]"))
    group.add_option('-H','--hour',dest='hour',type='str',
                      help=("hours to set the calendar. "
                      "[format from:to  default: '0:23']"))
    group.add_option('-M','--minutes',dest='minutes',type='str',
                      help=("minutes to set the calendar. "
                            "[format from:to  default: '0:59']"))
    group.add_option('-N','--num_proc',dest='np',type='int',
                      help=("Integer which specify the number of processes to "
                            "set to the calendar) [no Default Value]"))
    parser.add_option_group(group)
    
        
    (opts, _) = parser.parse_args()
    
    
    clients = [socket.gethostname()]
    if opts.clients is not None:
        clients = opts.clients.split(",")
    
    ok, data = handle_request('GET_CONFIGS',clients)
    if ok:
        ConfigsReceived = data

    notmatched =  set(clients) - ConfigsReceived.keys()
    if notmatched:
        print("These clients: " + ", ".join(notmatched) + "\n do not exist "
              "in the server's list.")
        return
    
    calendars = {}
    if opts.calendar in {'append','set'}:
        if opts.np is None:
            print('Calendar not submitted: must specify -N or --num_proc option')
            return 
        else:
            np = opts.np
    
        if opts.week is not None:
            week = opts.week.split(',')
            days = tuple(x for x in calendar.day_name for y in week 
                                    if x.lower().startswith(y.lower()))
            if len(days) != len(week):
                print("Problem with at least one week day specified")
                return
        else:
            days = (calendar.day_name[datetime.datetime.now().weekday()],)
        
        if opts.hour is not None:
            hour = tuple(int(x) for x in opts.hour.split(':'))
            if len(hour) != 2 or  not all(-1 < x < 24 for x in hour):
                print("Problem with specification of hour")
                return
            y = 1 if hour[0]<=hour[1] else 25
            hour = tuple(x % 24 for x in range(hour[0],hour[1] + y))
        else:
            hour = tuple(x for x in range(24))
        
        if opts.minutes is not None:
            minutes = tuple(int(x) for x in opts.minutes.split(':'))
            if len(minutes) != 2 or  not all(-1 < x < 60 for x in minutes):
                print("Problem with specification of minutes")
                return
            y = 1 if minutes[0] <= minutes[1] else 61
            minutes = (x % 60 for x in range(minutes[0], minutes[1] + y))
        else:
            minutes = tuple(range(60))   
        
        calendars = {(x,y,z): np for x in days for y in hour for z in minutes}
    else:
        if opts.calendar is not None:
            print("Wrong value for --calendar option:", opts.calendar)
            return
        if any((opts.minutes, opts.hour, opts.week)):
            print("Option --calendar must be given to set the calendar")
            return
    
    for k in ConfigsReceived.keys():
        if opts.calendar == 'append':
            ConfigsReceived[k].Calendar.update(calendars)
        elif opts.calendar == 'set':
            ConfigsReceived[k].Calendar = calendars
    
    
    if opts.niceness is not None:
        niceness = (-20 if -20 > opts.niceness else 
                     20 if  20 < opts.niceness else opts.niceness )
        for k in ConfigsReceived.keys():
            ConfigsReceived[k].niceness = niceness
    
    if opts.shut is not None:
        if not opts.shut:
            print('Option -s must be True or False')
            return
        shut = (True  if  'true'.startswith(opts.shut.lower()) else
                False if 'false'.startswith(opts.shut.lower()) else 'bla' )
        if shut == 'bla':
            print('Option -s must be True or False')
            return
        for k in ConfigsReceived.keys():
            ConfigsReceived[k].shutdown = shut
        
    if opts.More is not None:
        if not opts.More:
            print('Option -s must be True or False')
            return
        More = (True  if  'true'.startswith(opts.More.lower()) else
                False if 'false'.startswith(opts.More.lower()) else 'bla' )
        if More == 'bla':
            print('Option -s must be True or False')
            return
        for k in ConfigsReceived.keys():
            ConfigsReceived[k].MoreJobs = More
        
        
    if opts.defproc is not None:
        defproc = opts.defproc
        for k in ConfigsReceived.keys():
            ConfigsReceived[k].defNumJobs = defproc
    
    
    ok, clients = handle_request('SET_CONFIGS',ConfigsReceived)
    if ok:
        print('Success. Configurations will be set!')
    else:
        print("It seems that these clients are not in the server's list;",
              ', '.join(clients))
        
        
        
if __name__ == '__main__':
    main()
