#!/usr/bin/env python3

import optparse
import calendar
import Global

def main():
    # configuration of the parser for the arguments
    parser = optparse.OptionParser()
    parser.add_option('-c','--clients',dest='clients',type='str',
                      help="list of hosts to get the configs. [format: "
                      "client1,client2,...  default: 'all']" + Global.MATCH_RULE)
    parser.add_option('--showCalendar',dest='sCal',action='store_true',
                      help="Show the calendar of each client", default=False)
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
  
    if opts.sCal:
        sortCal = lambda x:(getattr(calendar,x[0][0].upper()),x[0][1],x[0][2])
        sorTab = lambda x:getattr(calendar,x[0].upper())
        days = tuple(x for x in calendar.day_name)
        hours = tuple(range(24))
        minutes = tuple(range(60))
        print(' '*14, calendar.weekheader(9))
        for k, v in sorted(ConfigsReceived.items(),key=lambda x: x[0]):
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
                print('{:^15s}{:s}'.format('{0:02d}:{1:02d}'
                                           .format(kl[0], kl[1]),nums))  
        return
    
    print('{:15s}{:^7s}{:^9s}{:^9s}{:^10s}{:^6s}'
          .format('hostname','state', 'numcpus','NumJobs',
                  'MoreJobs', 'Nice'))
    for k,v in sorted(ConfigsReceived.items(),key=lambda x: x[0]):
        print('{0:15s}{1.active!s:^7s}{1.numcpus:^9d}{1.defNumJobs:^9d}'
              '{1.MoreJobs!s:^10}{1.niceness:^6d}'
              .format(k,v))
        
        
        
if __name__ == '__main__':
    main()

