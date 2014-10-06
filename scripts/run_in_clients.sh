#!/usr/bin/env python3

import optparse
import calendar
import datetime
import Global

def main():
    # configuration of the parser for the arguments
    parser = optparse.OptionParser()
    parser.add_option('-c','--clients',dest='clients',type='str',
                      help="list of hosts to get the configs. [format: "
                      "client1,client2,...  default: 'all']" + Global.MATCH_RULE)
    parser.add_option('-s','--state',dest='state',type='str',
                      help="run the script only in clients with the given "
                      "states. [possible_values: 'on','off','dead' "
                      "default: 'on']. To select more than one state, "
                      "separate the values with comma."
    (opts, _) = parser.parse_args()
    
    try:
        if opts.clients == 'all' or opts.clients is None:
            clients = opts.clients
            ok, ConfigsReceived = Global.handle_request('GET_CONFIGS','all')
        else:
            clients = set(opts.clients.split(","))
            ConfigsReceived = Global.match_clients(clients)
            ok = True
        if not ok:
            raise MatchClientsErr('Could not get configs of server.')
    except Global.MatchClientsErr as err:
        print(err)
        return
  import paramiko
import cmd

class RunCommand(cmd.Cmd):
    """ Simple shell to run a command on the host """

    prompt = 'ssh > '

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.hosts = []
        self.connections = []

    def do_add_host(self, args):
        """add_host 
        Add the host to the host list"""
        if args:
            self.hosts.append(args.split(','))
        else:
            print "usage: host "

    def do_connect(self, args):
        """Connect to all hosts in the hosts list"""
        for host in self.hosts:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(
                paramiko.AutoAddPolicy())
            client.connect(host[0], 
                username=host[1], 
                password=host[2])
            self.connections.append(client)

    def do_run(self, command):
        """run 
        Execute this command on all hosts in the list"""
        if command:
            for host, conn in zip(self.hosts, self.connections):
                stdin, stdout, stderr = conn.exec_command(command)
                stdin.close()
                for line in stdout.read().splitlines():
                    print 'host: %s: %s' % (host[0], line)
        else:
            print "usage: run "

    def do_close(self, args):
        for conn in self.connections:
            conn.close()

if __name__ == '__main__':
    RunCommand().cmdloop()

