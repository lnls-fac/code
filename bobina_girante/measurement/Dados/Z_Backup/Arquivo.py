import sys
import numpy

f=open('Fonte_130A.dat','r')
config = f.read().split('\n')
f.close()

d=config
for i in range(len(config)):
    c=config[i].split('\t')
    d[i]=c[1]
