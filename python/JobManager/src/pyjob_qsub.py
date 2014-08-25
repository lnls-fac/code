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
    # Begin the creation of the job
    job = Global.Jobs()
    
    # configuration of the parser for the arguments
    parser = optparse.OptionParser()
    parser.add_option('-d','--description',dest='description',type='str',
                      help="description of the job [default: 'generic job']")
    parser.add_option('-e','--exec',dest='exec_script_name',type='str',
                      help=("name of the script to run in the cluster "
                            "[no Default, mandatory]"))
    parser.add_option('-i','--inputFiles',dest='input_file_names',type='str',
                      help=("name of the input files needed to run the job."
                            " For more than one file, separate the names with"
                            " commas and no space. [default: '']"))
    parser.add_option('-w','--workingDirectory',dest='work_dir',type='str',
                      help=("Working directory of the job: where the execution"
                            " file and input files are and the results will "
                            "be put [default: pwd]"))
    parser.add_option('-p','--priority',dest='prior',type='int',
                      help=("Integer which specify the priority of the job. "
                            "Higher numbers have higher priority (negative allowed)"
                            "[default: 0]"))
    
    (opts, _) = parser.parse_args()
        
    # Load execution script
    if opts.exec_script_name is None:
        print('Job not submitted: must specify -e or --exec option')
        return 
    else:
        data = Global.load_file(opts.exec_script_name)
        if data is not None:
            job.execution_script.update({opts.exec_script_name:data})
        else:
            sys.exit(1)
    #Load name
    if opts.description is not None:
        job.description = opts.description
    
    #Load working_dir
    if opts.work_dir is not None:
        job.working_dir = os.path.abspath(opts.work_dir)
    
    #Load priority
    if opts.prior is not None:
        if isinstance(opts.prior, int):
            job.priority = int(float(opts.prior))
        else:
            print('Could not set the priority. Using default')
    
    if opts.input_file_names is not None:
        input_file_names = opts.input_file_names.split(',')
        for name in input_file_names:
            data = Global.load_file(name)
            if data is not None:
                job.input_files.update({name: data})
            else:
                sys.exit(1)
    
    ok, data = handle_request('NEW_JOB',job)
    
    if ok:
        print('Success. Job id is :', data)
    
    
    
main()