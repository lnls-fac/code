#!/usr/bin/env python3

import optparse
import Global

def main():
    # configuration of the parser for the arguments
    parser = optparse.OptionParser()
    group = optparse.OptionGroup(parser, "Job Selection Options")
    group = Global.job_selection_parse_options(group)
    parser.add_option_group(group)
    group = optparse.OptionGroup(parser, "Signals Options")
    group.add_option('-S', '--signal', dest='signal', type='str',
                     help="Send signal to jobs. Options are: kill, pause or " 
                     "continue")
    group.add_option('-P', '--priority', dest='priority', type='int',
                     help="Change priority of jobs. Must be an integer")
    group.add_option('-H', '--possibleHosts', dest='hosts', type='str',
                     help="Change the list of possible hosts to run the"
                     "jobs [format: append=host1,host2,... or set=host1,host2"
                     ",..." + Global.MATCH_RULE)
    group.add_option('-Q', '--queue', dest='queue', action='store_true',
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
    
    try:
        Queue = Global.job_selection_parse(opts)
    except Global.JobSelParseErr as err:
        print(err)
        return

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
        if action[1] != 'all':
            keys2Match = set(action[1].split(','))
            try:
                hosts = set(Global.match_clients(keys2Match).keys())
            except Global.MatchClientsErr as err:
                print(err)
                return
        else:
            hosts = 'all'
        for k,v in Queue.items():
            if hosts == 'all':
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
        
    ok, data1, data2 = Global.handle_request('CHANGE_JOBS_REQUEST',Queue)

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
