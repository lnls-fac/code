#!/usr/bin/python

#import sys

#sys.path.append('/home/ximenes/workspace')

import pyring.tracking
import ring_v403

the_ring = ring_v403.create_lattice(mode = 'AC10', energy = 3e9)

pyring.tracking.default_server = pyring.tracking.servers['pyring']

pos = pyring.pos(0.001,0,0,0,0,0)
r = pyring.tracking.track1turn(the_ring, pos) 
print(r)



#e1 = pyring.elements.drift(fam_name = 'drift', length = 1.3)
#print(e1)