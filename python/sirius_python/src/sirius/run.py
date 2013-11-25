#!/usr/bin/python

# importing libraries from bash
# -----------------------------
#import sys
#sys.path.append('/home/ximenes/workspace')

import ring_v403
import pyring.tracking
import pyring.lattice
import time
import matplotlib.pyplot as plt

''' load lattice model
    ------------------ '''
the_ring = ring_v403.create_lattice(mode = 'AC10', energy = 3e9)
the_ring = the_ring[::] # option to select subset of elements
pyring.lattice.setcavity(the_ring, 'off')
#pyring.lattice.printlattice(the_ring)


''' parameters '''
nr_particles = 1
nr_turns     = 100

''' selection of tracking method and initial conditions '''
pos = nr_particles*[0.009,0.0000,0.0,0.0,0.0,0.0]
#pyring.tracking.default_server = pyring.tracking.servers['pyring']
pyring.tracking.default_server = pyring.tracking.servers['trackcpp']


''' timed tracking '''
t0 = time.time()
#p = pyring.tracking.tracknturns(the_ring, pos, nr_turns = 20, turn_by_turn = True, trajectory = False)
#p = pyring.tracking.track1turn(the_ring, pos, trajectory = False)
p = pyring.tracking.tracknturns(the_ring, pos = pos, nr_turns = nr_turns, turn_by_turn = True, trajectory = False)
t1 = time.time()
print(t1-t0)
print(len(p))

''' selects result data '''
p1 = pyring.tracking.get_particle(pos = p, nr_particles = nr_particles, nr_elements = 1, nr_turns = nr_turns, particle = 0)
rx = pyring.tracking.get_rx(p1)
px = pyring.tracking.get_px(p1)
# 
''' plots result '''
plt.scatter(rx,px)
plt.show()






    
#while True:
#    pass
#pos = pyring.tracking.track1turn(the_ring, pos)
#print([pos[0], pos[6]])



#e1 = pyring.elements.drift(fam_name = 'drift', length = 1.3)
#print(e1)