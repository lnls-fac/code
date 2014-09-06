#!/usr/bin/env python3

import optparse
import Global

STATUS = Global.STATUS

def main():
    parser = optparse.OptionParser()
    parser = Global.job_selection_parse_options(parser)
    parser.set_description(description='This command lists the jobs in the '
                           ' queue.')
    
    (opts, _) = parser.parse_args()
    
    try:
        Queue = Global.job_selection_parse(opts)
    except Global.JobSelParseErr as err:
        print(err)
        return
    
    print('{:8s}{:^5s}{:^8s}{:^10s}{:^20s}{:^16s}{:^16s}{:^16s}'
      .format('Job ID','Prior', 'Status','User',
              'Description', 'Host Owner','Host Running','Possible Hosts'))
    for k,v in Queue.items():
        print('{0:^8}{1.priority:^5d}{1.status_key:^8s}{1.user:^10s}'
              '{1.description:20s}{1.hostname:^16s}{2:^16s}'
              .format(k, v, v.runninghost or 'None'), v.possiblehosts)

    
if __name__ == '__main__':
    main()