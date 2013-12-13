import pos
import passmethods
import trackcpp
import numpy

def linepass (line, particles, refpts = None, element_offset = 0, engine = 'trackcpp'):
    
    ''' process arguments '''
    if refpts is None:
        trajectory = False
    else:
        trajectory = True
        if (type(refpts) is not list) and (type(refpts) is not tuple):
            refpts = [refpts]
            
    ''' does tracking according to selected engine '''
    if engine == 'pyring':
        pos_out = _Tracking.linepass_pyring(line, particles, trajectory, element_offset)
    elif engine == 'trackcpp':
        pos_out = _Tracking.linepass_trackcpp(line, particles, trajectory, element_offset)
    else:
        raise Exception('tracking engine not defined|implemented!')
    
    ''' returns data '''
    if trajectory:
        return select(pos_out, nr_particles = particles.shape[1], nr_elements = len(line)+1, nr_turns = 1, element = refpts)
    else:
        return pos_out
        
    
def ringpass (ring, particles, nr_turns = 1, element_offset = 0, engine = 'trackcpp'):
    if engine == 'pyring':
        return _Tracking.ringpass_pyring(ring, particles, nr_turns, element_offset)
    elif engine == 'trackcpp':
        return _Tracking.ringpass_trackcpp(ring, particles, nr_turns, element_offset)
    else:
        raise Exception('tracking server not defined|implemented!')
    
def lost (particles, nr_particles = 1, nr_elements = 1, nr_turns = 1):
    
    if particles.shape[1] != (nr_turns * nr_elements * nr_particles):
        raise Exception('pyring.tracking.lost: invocation with inconsistent parameters')
    
    (_,lost_idx) = numpy.nonzero(numpy.isnan(particles))
    if len(lost_idx) != 0:
        first_lost_idx = lost_idx[0] # first lost particle
        (turn, element, particle) = numpy.unravel_index(first_lost_idx, (nr_turns, nr_elements, nr_particles))
        return (turn, element, particle)
    else:
        return ()
    
    
def select(particles, nr_particles = 1, nr_elements = 1, nr_turns = 1, particle = None, element = None, turn = None):
    
    if particles.shape[1] != (nr_turns * nr_elements * nr_particles):
        raise Exception('pyring.tracking.get_data: invocation with inconsistent parameters') 
    
    if particle is None:
        particle = range(nr_particles)
    else:
        if (type(particle) is not list) and (type(particle) is not tuple):
            particle = [particle]
    if element is None:
        element = range(nr_elements)
    else:
        if (type(element) is not list) and (type(element) is not tuple):
            element = [element]
    if turn is None:
        turn = range(nr_turns)
    else:
        if (type(turn) is not list) and (type(turn) is not tuple):
            turn = [turn]
  
    ''' builds index vector '''          
    tuplesl = numpy.array([(turn_,element_,particle_) for turn_ in turn for element_ in element for particle_ in particle], dtype = 'int')
    mfactor = numpy.array([(nr_elements*nr_particles,nr_particles,1) for turn_ in turn for element_ in element for particle_ in particle], dtype = 'int')        
    indices = (tuplesl * mfactor).sum(axis=1)
    
    return particles[:, indices]
    


    
class _Tracking:
    
    @staticmethod
    def num2py(pos):
        return numpy.reshape(pos, pos.size, order='F').tolist()
    
    @staticmethod
    def py2num(pos):
        return numpy.reshape(numpy.array(pos), (6,-1), order='F')


    @staticmethod
    def linepass_pyring(line, particles, trajectory, element_offset):
        
        nr_particles = particles.shape[1] 
        nr_elements  = len(line)
        (rx,px) = (particles[0,:], particles[1,:])
        (ry,py) = (particles[2,:], particles[3,:])
        (de,dl) = (particles[4,:], particles[5,:])
         
        if trajectory:
            ''' case: records all trajectory ---'''
            new_particles = numpy.zeros((6, (nr_elements+1) * nr_particles))
            np = pos.Pos(rx,px,ry,py,de,dl)
            e = element_offset % nr_elements # works even when offset > nr_elements
            for i in range(nr_elements):
                ''' records particle coordinates (at entrance) '''
                (i1,i2) = (i*nr_particles, (i+1)*nr_particles) 
                (new_particles[0, i1:i2], new_particles[1, i1:i2]) = (np.rx, np.px)
                (new_particles[2, i1:i2], new_particles[3, i1:i2]) = (np.ry, np.py)
                (new_particles[4, i1:i2], new_particles[5, i1:i2]) = (np.de, np.dl)
                ''' tracks through element '''
                (_, pm_map) = passmethods.pm_dict[line[e].pass_method]
                pm_map(np, line[e]) 
                e = (e + 1) % nr_elements
            ''' records particle coordinates (at end) '''
            i = nr_elements
            (i1,i2) = (i*nr_particles, (i+1)*nr_particles) 
            (new_particles[0, i1:i2], new_particles[1, i1:i2]) = (np.rx, np.px)
            (new_particles[2, i1:i2], new_particles[3, i1:i2]) = (np.ry, np.py)
            (new_particles[4, i1:i2], new_particles[5, i1:i2]) = (np.de, np.dl)
        else:
            ''' case: records only at end of line '''
            new_particles = numpy.zeros((6, nr_elements * nr_particles))
            np = pos.Pos(rx,px,ry,py,de,dl)
            e = element_offset % nr_elements # works even when offset > nr_elements
            for _ in range(nr_elements): 
                ''' tracks through element '''
                (_, pm_map) = passmethods.pm_dict[line[e].pass_method]
                pm_map(np, line[e])
                e = (e + 1) % nr_elements
            ''' records particle coordinates (at exit) ''' 
            (new_particles[0, :], new_particles[1, :]) = (np.rx, np.px)
            (new_particles[2, :], new_particles[3, :]) = (np.ry, np.py)
            (new_particles[4, :], new_particles[5, :]) = (np.de, np.dl)
                
        return new_particles

    @staticmethod
    def ringpass_pyring(ring, particles, nr_turns, element_offset):
        
        nr_particles = particles.shape[1]
        
        new_particles = numpy.zeros((6, nr_turns * nr_particles))
        for t in range(nr_turns):
            particles = _Tracking.linepass_pyring(ring, particles, trajectory = False, element_offset = element_offset)
            new_particles[:,(t*nr_particles):((t+1)*nr_particles)] = particles
        return new_particles
    
    @staticmethod
    def linepass_trackcpp(lattice, particles, trajectory, element_offset): 
        return _Tracking.py2num(trackcpp.linepass(lattice, _Tracking.num2py(particles), trajectory, element_offset))
    
    @staticmethod
    def ringpass_trackcpp(lattice, particles, nr_turns, element_offset):
        return _Tracking.py2num(trackcpp.ringpass(lattice, _Tracking.num2py(particles), nr_turns, element_offset))


    
