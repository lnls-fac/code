#!/bin/bash

host="JobClient"

function dostop()
{
    ## check if WinXP is running
    vboxmanage showvminfo $host --machinereadable | grep -q 'VMState="running"' &> /dev/null
    if [ $? -ne 0 ]; then
        echo $host "not running"
        exit
    fi
    ## try gracefully savestate
    echo -n "Shutting down JobClient ... "
    pid=$( vboxmanage guestcontrol $host  execute --image /bin/ps --username fac \
                                --password 2f0a1c4 --wait-stdout -- -elf | \
         grep pyjob_run.py | grep -o "fac[ ]*\b[0-9]\{2,5\}\b" | grep -o "[0-9]\{2,5\}" )
     
    echo "The JobClient's pid is: " $pid
    
    vboxmanage guestcontrol $host  execute --image /bin/kill --username fac \
                                --password 2f0a1c4 --wait-stdout -- -USR1 $pid
    sleep 1
    vboxmanage controlvm $host savestate
    
    ## check vm status
    INDEX=7
    while [ $INDEX -gt 0 ]; do
        echo -n "$INDEX "
        vboxmanage showvminfo $host --machinereadable | grep -q 'VMState="running"' &> /dev/null
        if [ $? -ne 0 ]; then
            echo "gracefully done"
            break
        fi
        sleep 1
        let INDEX+=-1
    done
    ## close forcefully
    if [ $INDEX -eq 0 ]; then
        vboxmanage controlvm $host poweroff &> /dev/null
        echo "forcefully done"
    fi
}
export -f dostop

dostop

