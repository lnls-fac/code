#!/usr/bin/env python3

import optparse
import Global

STATUS = Global.STATUS

EXPLICATION = dict(q='In the queue',
              qu='The user scheduled the job back to the queue but the'
              'signal was not sent to the host which is running the job yet.',
              r='Running',
              ru='Scheduled to continue by user, but the signal has not '
              'reached the host of the job.',
              p='Paused',
              pu='Job paused by the user. The only way to continue this job is'
              "through a 'continue' command with pyjob_qsig.py.",
              w='The job was sent to the host for running, but it has not '
              'initiated yet. This status will only appear when the host is a'
              'cluster, such as sgi or sunhpc.',
              t='The job was terminated anomalously. Possible causes are: user'
              'command, host reboot, power outage.',
              tu="The user terminated the job, but the signal hasn't been "
              'sent to the host.',
              e='Job ended successfully.',
              s='Job has been sent to the host, but its current status was not'
              ' confirmed yet.',
              ch='User scheduled some change in the job priority or possible '
              'hosts to run it, but the confirmation of such action was not '
              'received yet.')

def main():
    parser = optparse.OptionParser()
    parser = Global.job_selection_parse_options(parser)
    parser.set_description(description='This command lists the jobs in the '
                           ' queue.')
    parser.add_option('--explicate',dest='explicate', action='store_true',
                      help="This option explains the meaning of the several "
                      "status flag of the jobs.", default=False)
    
    (opts, _) = parser.parse_args()
    
    if opts.explicate:
        print('{:^6s}{:^74s}'.format('STATUS', 'EXPLICATION'))
        for k,v in sorted(EXPLICATION.items(),key=lambda x:x[0]):
            v = v.split()
            print('{:^6s}{}'.format(k,v[0]),end=' ')
            leng = len(v[0])
            for ii in range(1,len(v)):
                leng += len(v[ii])
                if leng <= 74:
                    print(v[ii],end=' ')
                else:
                    leng = len(v[ii])
                    print('\n',' '*4,v[ii], end=' ')
            print('\n')
        return
    
    
    try:
        Queue = Global.job_selection_parse(opts)
    except Global.JobSelParseErr as err:
        print(err)
        return
    
    if Queue:
        print('{:8s}{:^5s}{:^8s}{:^10s}{:^20s}{:^16s}{:^16s}{:^16s}'
          .format('JobID','Prior', 'Status','User',
                  'Description', 'Host Owner','Host Running','Possible Hosts'))
    for k,v in Queue.items():
        print('{0:^8}{1.priority:^5d}{1.status_key:^8s}{1.user:^10s}'
              '{1.description:20s}{1.hostname:^16s}{2:^16s}'
              .format(k, v, v.runninghost or 'None'), v.possiblehosts)

    
if __name__ == '__main__':
    main()