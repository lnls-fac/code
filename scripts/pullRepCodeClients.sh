#!/usr/bin/env python3

import subprocess

res = subprocess.getoutput('pyjob_configs_get.py').splitlines()[1:]
print(res)
for re in res:
    r = re.split()
    #if r[1] == 'on':
    subprocess.call(['ssh', r[0], 'cd /home/fac_files/code && git pull '])
#    subprocess.call(['ssh', r[0], "rm -r /home/fac_files/code/python/JobManager/.TempFolders/*"])
