#! /bin/bash -e

function dostart()
{
    echo -n "Running JobClient ... "
    vboxheadless --startvm JobClient
    echo "now closed"
}
export -f dostart

dostart



