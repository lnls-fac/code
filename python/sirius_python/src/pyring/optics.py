import mathphysicslibs.constants as mpconsts
import lattice
import tracking
import numpy

    
def findorbit6(ring, refpts = None, guess = None, max_iterations = 20, step_size = 1e-9):
    
    ''' process arguments '''
    if refpts is None:
        refpts = [0]
    Ri = [0,0,0,0,0,0]
    if guess is not None:
        Ri = guess
        
    ''' period '''
    l0 = lattice.findspos(ring)
    c0 = mpconsts.light_speed
    t0 = l0/c0
    
    ''' revolution freq. and harmonic number '''
    cav_idx = lattice.findcells(ring, 'frequency'); cav_idx = cav_idx[0] # chooses first cavity
    rev_freq = ring[cav_idx].frequency
    hnumber = ring[cav_idx].hnumber
    theta = numpy.zeros((6,1)); theta[5] = c0*(hnumber/rev_freq - t0)
    
    D = step_size * numpy.eye(6,7)
    RMATi = numpy.zeros((6,7))
    for i in range(7):
        RMATi[:,i] = Ri
    RMATi += D
    RMATf = tracking.track1turn(lattice = ring, pos = RMATi, trajectory = False, engine = 'trackcpp')
    J6 = (RMATf[:,-1]-RMATf(:,7)*ones(1,6))/d;
    
    print('ok')
    
    
        