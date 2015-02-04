#!/bin/bash

# descubro o ip da máquina
ip=$( ifconfig | grep -A 2 eth0 | grep "inet add" | cut --delimiter=":" -f 2 | cut --delimiter="B" -f 1 )
if [ -z "$ip" ]; then
    ip=$( ifconfig | grep -A 2 eth1 | grep "inet add" | cut --delimiter=":" -f 2 | cut --delimiter="B" -f 1 )
fi

ip=${ip//[[:blank:]]/}

# descubro o hostname da máquina
host=$( hostname -s )
# descubro qual o ip que está escrito no hostfile
iphf=$( grep $host /etc/hosts | tail -n +2 | cut --delimiter=${host:0:1} -f 1 )
iphf=${iphf//[[:blank:]]/}

# A partir do ip descubro todos os nomes da máquina que 
# estão definidos no hostfile e substituo o ip antigo pelo ip novo
grep $iphf /etc/hosts | sed -e "s/$iphf/$ip/g" > ~/$host

# copio o arquivo para a workstation e removo o arquivo local
scp ~/$host workstation-linux:~/ips_clients/
rm ~/$host


