#!/usr/bin/python

import ring_v500
import pyring.tracking
import pyring.lattice
import pyring.optics
#import time
import matplotlib.pyplot as plt
import numpy

def test_linepass(the_ring):
    
    ''' set cavity state '''
    the_ring = pyring.lattice.copy.deepcopy(the_ring)
    the_ring = pyring.lattice.setcavity(the_ring, 'off')
    
    #s = pyring.lattice.findspos(lattice = the_ring, indices = range(len(the_ring)))
    
    nr_particles = 2
    refpts = [0,1500-1,len(the_ring)]
    posi = numpy.zeros((6,nr_particles))
    posi[:,0] = [0.001,0,0,0,0,0]
    posi[:,1] = [0.002,0,0,0,0,0]
    posf = pyring.tracking.linepass(lattice = the_ring, particles = posi, refpts = refpts, engine = 'pyring')
    
    for i in range(posf.shape[0]):
        for j in range(posf.shape[1]):
            print('{:+22.16E} '.format(posf[i,j])),
        print('')
#     plt.plot(s, 1000*posf[0,:])
#     plt.xlabel('s [m]'); plt.ylabel('x [mm]')
#     plt.show()
    
def test_ringpass(the_ring):
    
    nr_turns = 1000
    posi = numpy.array([[0.001],[0],[0],[0],[0],[0]])
    posf = pyring.tracking.ringpass(ring = the_ring, particles = posi, nr_turns = nr_turns, engine = 'trackcpp')
    

    
    for i in range(posf.shape[0]):
        for j in range(posf.shape[1]):
            print('{:+22.16E} '.format(posf[i,j])),
        print('')
        
    plt.scatter(1000*posf[0,:],1000*posf[1,:])
    plt.xlabel('x [mm]'); plt.ylabel('xl [mrad]')
    plt.show()          
    
def test_findorbit4(the_ring):
    
    ''' set cavity state '''
    the_ring = pyring.lattice.copy.deepcopy(the_ring)
    the_ring = pyring.lattice.setcavity(the_ring, 'off')
    
    ''' introduces an horizontal kick '''
    hcms = pyring.lattice.findcells(the_ring, 'fam_name', 'hcm')
    the_ring[hcms[0]].kick_angle[0] = 0.0003;
    
    orb = pyring.optics.findorbit4(the_ring, de = 0, refpts = range(len(the_ring)))
    print('4D Closed orbit at beginning of model:')
    print('x  [mm]  : {0}'.format(orb[0,0]))
    print('xl [mrad]: {0}'.format(orb[1,0]))
    print('y  [mm]  : {0}'.format(orb[2,0]))
    print('yl [mrad]: {0}'.format(orb[3,0]))
    
    s = pyring.lattice.findspos(lattice = the_ring, indices = range(len(the_ring)))
    plt.scatter(s, 1000*orb[0,:])
    plt.show()
    
    print('ok')
    
    
def create_the_ring_sirius():
    
    the_ring = ring_v500.create_lattice(mode = 'AC10_6', energy = 3e9)
    the_ring = the_ring[::] # option to select subset of elements
    pyring.lattice.setcavity(the_ring, 'off')
    return the_ring

def create_the_ring_test():
    
    dipole = pyring.elements.rbend(fam_name = 'bend', length = 0.614131, angle = 0.035809880194256, angle_in = 0.035809880194256, angle_out = 0.0, nr_steps = 18, polynom_b = [0,-0.78]) 
    the_ring = [dipole]
    return the_ring

def run_tests():
    
            
    ''' load lattice model
        ------------------ '''
    the_ring = create_the_ring_sirius()
    #the_ring = create_the_ring_test()
    #pyring.lattice.printlattice(the_ring)
    
    
    test_linepass(the_ring)
    #test_ringpass(the_ring)
    #test_findorbit4(the_ring)
    
    
#     pyring.lattice.setcavity(the_ring, 'on')
#     orb2 = pyring.optics.findorbit6(the_ring)
#     
#     
#     
#     print(1e3*orb2)
#     
#     ''' parameters '''
#     nr_particles = 1
#     nr_turns     = 1000
#     
#     ''' selection of tracking method and initial conditions '''
#     pos = numpy.zeros((6,nr_particles))
#     pos[:,0] = [0.003, 0, 0, 0, 0, 0]   
#     
#     ''' timed tracking '''
#     t0 = time.time()
#     p = pyring.tracking.tracknturns(the_ring, pos = pos, nr_turns = nr_turns, turn_by_turn = True, trajectory = False)
#     t1 = time.time()
#     print('Total time: {0}'.format(t1-t0))
#     
#     ''' selects result data '''
#     p1 = pyring.tracking.get_particle(pos = p, nr_particles = nr_particles, nr_elements = 1, nr_turns = nr_turns, particle = 0)
#     rx = pyring.tracking.get_rx(p1)
#     px = pyring.tracking.get_px(p1)
#     
#     ''' plots result '''
#     plt.scatter(rx,px)
#     plt.show()
# 
#     ''' timed tracking '''
#     t0 = time.time()
#     p = pyring.tracking.tracknturns(the_ring, pos = pos, nr_turns = nr_turns, turn_by_turn = True, trajectory = True)
#     t1 = time.time()
#     print('Total time: {0}'.format(t1-t0))
#     
#     ''' selects result data '''
#     p1 = pyring.tracking.get_element(pos = p, nr_particles = nr_particles, element = 0, nr_elements = len(the_ring), nr_turns = nr_turns)
#     rx = pyring.tracking.get_rx(p1)
#     px = pyring.tracking.get_px(p1)
#     plt.scatter(rx,px)
#     p1 = pyring.tracking.get_element(pos = p, nr_particles = nr_particles, element = 100, nr_elements = len(the_ring), nr_turns = nr_turns)
#     rx = pyring.tracking.get_rx(p1)
#     px = pyring.tracking.get_px(p1)
#     plt.scatter(rx,px)
#     plt.show()
    
    
''' TESTS for PyRing and TrackC++ '''
    
run_tests()
