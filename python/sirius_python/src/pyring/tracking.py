import pos
import passmethods
import trackcpp
import numpy

def linepass (lattice, pos, trajectory = False, engine = 'trackcpp'):
    if engine == 'pyring':
        return _Tracking.linepass_pyring(lattice, pos, trajectory)
    elif engine == 'trackcpp':
        return _Tracking.linepass_trackcpp(lattice, pos, trajectory)
    else:
        raise Exception('tracking engine not defined|implemented!')
    
def ringpass (lattice, pos, nr_turns = 1, turn_by_turn = False, engine = 'trackcpp'):
    if engine == 'pyring':
        return _Tracking.ringpass_pyring(lattice, pos, nr_turns, turn_by_turn)
    elif engine == 'trackcpp':
        return _Tracking.ringpass_trackcpp(lattice, pos, nr_turns, turn_by_turn)
    else:
        raise Exception('tracking server not defined|implemented!')
    

def num2py(pos):
    return numpy.reshape(pos, pos.size, order='F').tolist()
def py2num(pos):
    return numpy.reshape(numpy.array(pos), (6,-1), order='F')


def get_turn (pos, nr_particles = 1, nr_elements = 1, nr_turns = 1, turn = None):
    if pos.shape[1] != (nr_particles*nr_elements*nr_turns):
        raise Exception('inconsistent parameters in get_turn invocation')
    if turn is None:
        turn = nr_turns-1
    return pos[:,(turn*nr_elements*nr_particles):((turn+1)*nr_elements*nr_particles)]
def get_element (pos, nr_particles = 1, nr_elements = 1, nr_turns = 1, element = None):
    if pos.shape[1] != (nr_particles*nr_elements*nr_turns):
        raise Exception('inconsistent parameters in get_element invocation')
    if element is None:
        element = nr_elements-1
    selection = numpy.zeros((6,nr_turns*nr_particles))
    for t in range(nr_turns):
        selection[:,t*nr_particles::nr_elements] = pos[:,(t*nr_elements*nr_particles+element*nr_particles):(t*nr_elements*nr_particles+(element+1)*nr_particles)]
    return selection
def get_particle (pos, nr_particles = 1, nr_elements = 1, nr_turns = 1, particle = 0, ):
    if pos.shape[1] != (nr_particles*nr_elements*nr_turns):
        raise Exception('inconsistent parameters in get_particle invocation')
    return pos[:,particle::nr_elements]
def get_rx(pos):
    return pos[0,:]
def get_px(pos):
    return pos[1,:]
def get_ry(pos):
    return pos[2,:]
def get_py(pos):
    return pos[3,:]
def get_de(pos):
    return pos[4,:]
def get_dl(pos):
    return pos[5,:]



    
class _Tracking:
    
    @staticmethod
    def linepass_pyring(lattice, particles, trajectory):
        
        nr_particles = particles.shape[1] 
        (rx,px) = (particles[0,:], particles[1,:])
        (ry,py) = (particles[2,:], particles[3,:])
        (de,dl) = (particles[4,:], particles[5,:])
         
        if trajectory:
            ''' case: records all trajectory ---'''
            nr_elements   = len(lattice)
            new_particles = numpy.zeros((6, nr_elements * nr_particles))
            np = pos.Pos(rx,px,ry,py,de,dl)
            for e in range(len(lattice)): 
                (_, pm_map) = passmethods.pm_dict[lattice[e].pass_method]
                ''' tracks through element '''
                pm_map(np, lattice[e]) 
                ''' records particle coordinates '''
                (e1,e2) = (e*nr_particles, (e+1)*nr_particles) 
                (new_particles[0, e1:e2], new_particles[1, e1:e2]) = (np.rx, np.px)
                (new_particles[2, e1:e2], new_particles[3, e1:e2]) = (np.ry, np.py)
                (new_particles[4, e1:e2], new_particles[5, e1:e2]) = (np.de, np.dl)      
        else:
            ''' case: records only at end of line '''
            nr_elements   = 1
            new_particles = numpy.zeros((6, nr_elements * nr_particles))
            np = pos.Pos(rx,px,ry,py,de,dl)
            for e in range(len(lattice)): 
                (_, pm_map) = passmethods.pm_dict[lattice[e].pass_method]
                ''' tracks through element '''
                pm_map(np, lattice[e])
            ''' records particle coordinates ''' 
            (new_particles[0, :], new_particles[1, :]) = (np.rx, np.px)
            (new_particles[2, :], new_particles[3, :]) = (np.ry, np.py)
            (new_particles[4, :], new_particles[5, :]) = (np.de, np.dl)
                
        return new_particles

    @staticmethod
    def ringpass_pyring(lattice, particles, nr_turns, turn_by_turn):
        
        nr_particles = particles.shape[1]
        
        if turn_by_turn:
            new_particles = numpy.zeros((6, nr_turns * nr_particles))
            for t in range(nr_turns):
                particles = _Tracking.linepass_pyring(lattice, particles, trajectory = False)
                new_particles[:,(t*nr_particles):((t+1)*nr_particles)] = particles
        else:
            new_particles = numpy.zeros((6, nr_particles))
            for t in range(nr_turns):
                particles = _Tracking.linepass_pyring(lattice, particles, trajectory = False)
            new_particles = particles
            
        return new_particles
    
    @staticmethod
    def linepass_trackcpp(lattice, pos, trajectory):
        return py2num(trackcpp.linepass(lattice, num2py(pos), trajectory))
    
    @staticmethod
    def ringpass_trackcpp(lattice, pos, nr_turns, turn_by_turn, trajectory):
        return py2num(trackcpp.ringpass(lattice, num2py(pos), nr_turns, turn_by_turn, trajectory))


    
