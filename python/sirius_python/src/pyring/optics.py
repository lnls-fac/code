import mathphysicslibs.constants as mpconsts
import lattice
import tracking
import numpy

    
def findorbit4(ring, de = 0, refpts = None, guess = None, init_nr_turns = 20, tol = 1e-14, max_iterations = 15, return_6d = False):
    
    ''' builds a valid list of element indices '''
    if refpts is None:
        refpts = [0]
    try:
        refpts[0]
    except:
        refpts = [refpts]
        
    ''' builds initial guess coordinate vector '''
    Ri = numpy.zeros((6,1))
    Ri[:,0] = numpy.array([0,0,0,0,de,0])
    if guess is not None:
        Ri[:4,0] = guess[:4]
    Ri_next = numpy.zeros((6,1))
    
    ''' main loop '''
    while True:
        Rf = tracking.tracknturns(lattice = ring, pos = Ri, nr_turns = init_nr_turns, turn_by_turn = True, trajectory = False, engine = 'trackcpp')
        Ri_next[:,0] = numpy.mean(Rf,axis=1)
        
        ''' checks whether tracking is unstable '''
        if numpy.isnan(sum(Ri_next)):
            raise Exception('findorbit4: overflow in particle coordinates')
        
        ''' number of iterations exceeded? '''
        max_iterations -= 1
        if max_iterations < 0:
            raise Exception('findorbit4: max number of iterations reached')
        
        ''' tolerance achieved? '''
        delta = abs(Ri_next[[1,2,3,4],0] - Ri[[1,2,3,4],0])
        #print(max(delta))
        Ri = Ri_next
        if all(delta < tol):
            break;
        
        ''' next iteration '''
        init_nr_turns += 1
    
    ''' builds closed orbit at all specified locations ''' 
    if (len(refpts)>1) or (refpts[0] != 0):             
        Ri = tracking.track1turn(lattice = ring, pos = Ri, trajectory = True, engine = 'trackcpp')
        
    ''' returns 4d (default) or 6d closed orbit data '''
    if return_6d:
        return Ri[:,refpts]
    else:
        return Ri[:4,refpts]
    
    
def findorbit6(ring, refpts = None, guess = None, init_nr_turns = 20, tol = 1e-14, max_iterations = 15):
    
    ''' period '''
    l0 = lattice.findspos(ring)
    c0 = mpconsts.light_speed
    t0 = l0/c0
    
    ''' revolution freq. and harmonic number '''
    cav_idx = lattice.findcells(ring, 'frequency'); cav_idx = cav_idx[0] # chooses first cavity
    rev_freq = ring[cav_idx].frequency
    hnumber = ring[cav_idx].hnumber
    theta = numpy.zeros((6,1)); theta[5] = c0*(hnumber/rev_freq - t0)
        
    raise Exception('findorbit6: not implemented yet')