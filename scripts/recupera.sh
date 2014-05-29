#!/bin/bash

user=`whoami`
echo $user
 
for i in $( ls -X | grep -v recupera.sh ); do
    pasta=$i"/*";
    if [ -e $i"/fimdeproc" ]; then
        folder=($( more $i"/fimdeproc" | grep home | cut --delimiter=: -f 2- ))
        scp -pr $pasta $user@lnls82-linux":"$folder > /dev/null
        echo "data recovered in $i"
    else
       echo "calculations not ready in $i"
       continue;
    fi
done
