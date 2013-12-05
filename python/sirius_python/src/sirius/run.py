#!/usr/bin/python

# importing libraries from bash
# -----------------------------
#import sys
#sys.path.append('/home/ximenes/workspace')

import ring_v500
import pyring.tracking
import pyring.lattice
import pyring.optics
import time
import matplotlib.pyplot as plt

def example1():
  
    
    ''' load lattice model
        ------------------ '''
    the_ring = ring_v500.create_lattice(mode = 'AC10_6', energy = 3e9)
    the_ring = the_ring[::] # option to select subset of elements
    pyring.lattice.setcavity(the_ring, 'off')
    #pyring.lattice.printlattice(the_ring)
    
    pyring.optics.findorbit6(the_ring)
    
    ''' parameters '''
    nr_particles = 1
    nr_turns     = 1000
    
    ''' selection of tracking method and initial conditions '''
    pos = nr_particles*[0.003,0.0000,0.0,0.0,0.0,0.0]
       
    ''' timed tracking '''
    t0 = time.time()
    p = pyring.tracking.tracknturns(the_ring, pos = pos, nr_turns = nr_turns, turn_by_turn = True, trajectory = False)
    t1 = time.time()
    print('Total time: {0}'.format(t1-t0))
    
    ''' selects result data '''
    p1 = pyring.tracking.get_particle(pos = p, nr_particles = nr_particles, nr_elements = 1, nr_turns = nr_turns, particle = 0)
    rx = pyring.tracking.get_rx(p1)
    px = pyring.tracking.get_px(p1)
    # 
    ''' plots result '''
    plt.scatter(rx,px)
    plt.show()






''' Example1
    ========
    Tracks Sirius around 100 turns from init cond. x0 = 10mm and plots horizontal phase space ellipse
'''
example1()
