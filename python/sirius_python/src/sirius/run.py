#!/usr/bin/python

#import sys
#sys.path.append('/home/ximenes/workspace')

import pyring.tracking
import ring_v403

the_ring = ring_v403.create_lattice(mode = 'AC10', energy = 3e9)
the_ring = the_ring[::]

#pyring.lattice.printlattice(the_ring)

pyring.tracking.default_server = pyring.tracking.servers['trackcpp']

#pos = pyring.pos(0.001,0,0,0,0,0)
pos = 10000*[0.002,0.0,0.0,0.0,0.0,0.0]
for i in range(1000):
    print(i)
    pyring.tracking.track1turn(the_ring, pos) 
while True:
    pass
#pos = pyring.tracking.track1turn(the_ring, pos)
print([pos[0], pos[6]])



#e1 = pyring.elements.drift(fam_name = 'drift', length = 1.3)
#print(e1)