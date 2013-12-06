import mathphysicslibs.constants as mpconsts
import lattice
import tracking
import numpy

    
def findorbit4(ring, de = 0, refpts = None, guess = None, init_nr_turns = 20, tol = 1e-14, max_iterations = 15, turn_by_turn = False):
    
    ''' builds a valid list of element indices '''
    if refpts is None:
        refpts = [0]
    try:
        refpts[0]
    except:
        refpts = [refpts]
        
    ''' builds initial guess coordinate vector '''    
    Ri = numpy.zeros((6,1))
    Ri[:,0] = [0,0,0,0,de,0]
    if guess is not None:
        guess = numpy.array(guess)
        Ri[:4,0] = guess[:4,0]
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
    Rf = numpy.zeros((6,len(ring)+1))
    Rf[:,0] = Ri[:,0]
    if (len(refpts)>1) or (refpts[0] != 0):             
        Rf[:,1:] = tracking.track1turn(lattice = ring, pos = Ri, trajectory = True, engine = 'trackcpp')
        
    ''' returns 4d (default) or 6d closed orbit data '''
    if turn_by_turn:
        Ri = tracking.tracknturns(lattice = ring, pos = Ri, nr_turns = init_nr_turns, turn_by_turn = True, trajectory = False, engine = 'trackcpp')
        return Ri
    else:
        return Rf[:4,refpts]
    
    
def findorbit6(ring, refpts = None, guess = None, init_nr_turns = 20, tol = 1e-8, max_iterations = 15, step_de = 1e-4):
    
    ''' builds a valid list of element indices '''
    if refpts is None:
        refpts = [0]
    try:
        refpts[0]
    except:
        refpts = [refpts]
     
    if guess is None:
        guess = numpy.array([[0.0],[0.0],[0.0],[0.0],[0.0],[0.0]])
    
    de0 = guess[4,0]        
    iteration = 0
    while (step_de > tol):
        
        de1 = de0 - step_de/2
        pos = findorbit4(ring, de = de1, refpts = [0], guess = guess, init_nr_turns = init_nr_turns, tol = 1e-14, max_iterations = max_iterations, turn_by_turn = True)
        guess[:,0] = pos[:,0] 
        dl1 = pos[5,-1] - pos[5,0]
        
        
        de2 = de0 + step_de/2
        pos = findorbit4(ring, de = de2, refpts = [0], guess = guess, init_nr_turns = init_nr_turns, tol = 1e-14, max_iterations = max_iterations, turn_by_turn = True)
        guess[:4,0] = pos[:4,0]
        dl2 = pos[5,-1] - pos[5,0]
        
        de0 = de1 - (de2 - de1) * (dl1/(dl2-dl1)) # linear interpolation
        
        if ((dl1<=0)!=(dl2<=0)):  # if interval contains solution does bisection
            step_de /= 2.0
    
        iteration += 1
        #print((iteration, de0, step_de))
            
    de = 0.5 * (de1 + de2)
    Ri = findorbit4(ring, de = de, refpts = [0], guess = guess, init_nr_turns = init_nr_turns, tol = tol, max_iterations = max_iterations, turn_by_turn = True)
    Ri = Ri[:,0]
    Ri = tracking.track1turn(lattice = ring, pos = Ri, trajectory = True, engine = 'trackcpp')
    Ri = Ri[:, refpts]
    return Ri
    
    