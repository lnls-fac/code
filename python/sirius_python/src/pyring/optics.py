import mathphysicslibs.constants as mpconsts
import lattice
import tracking
import numpy
import math
import copy

class Twiss:
    def __init__(self):
        self.closed_orbit = numpy.zeros((6,1))
        self.alphax = None
        self.betax  = None
        self.mux    = 0
        self.etaxl  = 0
        self.etax   = 0
        self.alphay = None
        self.betay  = None
        self.muy    = 0
        self.etayl  = 0
        self.etay   = 0
    def __str__(self):
        r = ''
        r += 'closed orbit: ' + '{0[0][0]:+10.3e} {0[1][0]:+10.3e} {0[2][0]:+10.3e} {0[3][0]:+10.3e} {0[4][0]:+10.3e} {0[5][0]:+10.3e}'.format(self.closed_orbit) + '\n'
        r += 'mux         : ' + '{0:+10.3e}'.format(self.mux) + '\n'
        r += 'betax       : ' + '{0:+10.3e}'.format(self.betax) + '\n'
        r += 'alphax      : ' + '{0:+10.3e}'.format(self.alphax) + '\n'
        r += 'etax        : ' + '{0:+10.3e}'.format(self.etax) + '\n'
        r += 'etaxl       : ' + '{0:+10.3e}'.format(self.etaxl) + '\n'
        r += 'muy         : ' + '{0:+10.3e}'.format(self.muy) + '\n'
        r += 'betay       : ' + '{0:+10.3e}'.format(self.betay) + '\n'
        r += 'alphay      : ' + '{0:+10.3e}'.format(self.alphay) + '\n'
        r += 'etay        : ' + '{0:+10.3e}'.format(self.etay) + '\n'
        r += 'etayl       : ' + '{0:+10.3e}'.format(self.etayl) + '\n'
        return r 
        
def findorbit4(ring, de = 0, refpts = None, guess = None, max_nr_iters = 50, tolerance = 100*numpy.spacing(1), delta = 1e-8, engine = 'trackcpp'):
    """ returns the 4D closed orbit solution of the ring """
    
    co = numpy.matrix(numpy.zeros((6,5,)))
    co[4,:] = [de,de,de,de,de]
    if guess is not None:
        co[:4,0] = numpy.array(guess).reshape((4,1))
            
    d1 = numpy.matrix([[delta],[0],[0],[0],[0],[0]])
    d2 = numpy.matrix([[0],[delta],[0],[0],[0],[0]])
    d3 = numpy.matrix([[0],[0],[delta],[0],[0],[0]])
    d4 = numpy.matrix([[0],[0],[0],[delta],[0],[0]])
    
    change = 1e100
    nr_iter = 0;
    while (change > tolerance) and (nr_iter <= max_nr_iters):
        co[:,1] = co[:,0] + d1
        co[:,2] = co[:,0] + d2
        co[:,3] = co[:,0] + d3
        co[:,4] = co[:,0] + d4
        co2 = numpy.matrix(tracking.linepass(line = ring, particles = numpy.array(co), engine = engine))
        (Ri, Rf) = (co[:4,0], co2[:4,0])
        M = numpy.matrix(numpy.zeros((4,4)))
        M[:,0] = (co2[:4,1]-co2[:4,0])/delta
        M[:,1] = (co2[:4,2]-co2[:4,0])/delta
        M[:,2] = (co2[:4,3]-co2[:4,0])/delta
        M[:,3] = (co2[:4,4]-co2[:4,0])/delta
        IM = numpy.linalg.inv(numpy.eye(4,4) - M)
        new_co = Ri + IM * (Rf - Ri)
        change = numpy.linalg.norm(new_co - co[:4,0])        
        co[:4,0] = new_co
        nr_iter += 1
        
    co = co[:,0]
        
    if (nr_iter > max_nr_iters):
        raise Exception('findorbit4 did not converge!')
    
    if refpts is None:
        return co[:4,0]
    
    try:
        refpts[0]
    except:
        refpts = [refpts]
        
    orb = tracking.linepass(line = ring, particles = numpy.array(co), refpts = range(len(ring)+1), engine = engine)
    return orb[:4,refpts]    
            
    
def findorbit6(ring, refpts = None, guess = None, max_nr_iters = 50, tolerance = 100*numpy.spacing(1), delta = 1e-9, engine = 'trackcpp'):
    """ returns the 6D closed orbit solution of the ring """
    
    co = numpy.matrix(numpy.zeros((6,7,)))
    if guess is not None:
        co[:,0] = numpy.array(guess).reshape((6,1))
            
    d1 = numpy.matrix([[delta],[0],[0],[0],[0],[0]])
    d2 = numpy.matrix([[0],[delta],[0],[0],[0],[0]])
    d3 = numpy.matrix([[0],[0],[delta],[0],[0],[0]])
    d4 = numpy.matrix([[0],[0],[0],[delta],[0],[0]])
    d5 = numpy.matrix([[0],[0],[0],[0],[delta],[0]])
    d6 = numpy.matrix([[0],[0],[0],[0],[0],[delta]])
    
    L0 = lattice.findspos(ring, len(ring)+1)
    C0 = mpconsts.light_speed
    T0 = L0/C0 
    cav_idx = lattice.findcells(ring, 'frequency')
    frf = ring[cav_idx[0]].frequency;
    harm_number = ring[cav_idx[0]].hnumber
    theta = numpy.matrix([[0],[0],[0],[0],[0],[C0*(harm_number/frf - T0)]])
    
    dco = [1,1,1,1,1,1];
    nr_iter = 0;
    while (any(numpy.absolute(dco) > tolerance)) and (nr_iter <= max_nr_iters):
        co[:,1] = co[:,0] + d1
        co[:,2] = co[:,0] + d2
        co[:,3] = co[:,0] + d3
        co[:,4] = co[:,0] + d4
        co[:,5] = co[:,0] + d5
        co[:,6] = co[:,0] + d6
        co2 = numpy.matrix(tracking.linepass(line = ring, particles = numpy.array(co), engine = engine))
        (Ri, Rf) = (co[:,0], co2[:,0])
        M = numpy.matrix(numpy.zeros((6,6)))
        M[:,0] = (co2[:,1]-co2[:,0])/delta
        M[:,1] = (co2[:,2]-co2[:,0])/delta
        M[:,2] = (co2[:,3]-co2[:,0])/delta
        M[:,3] = (co2[:,4]-co2[:,0])/delta
        M[:,4] = (co2[:,5]-co2[:,0])/delta
        M[:,5] = (co2[:,6]-co2[:,0])/delta
        IM = numpy.linalg.inv(numpy.eye(6,6) - M)
        new_co = Ri + IM * (Rf - Ri - theta)        
        dco = new_co - co[:,0]
        co[:,0] = new_co
        print(new_co)
        nr_iter += 1
        
    co = co[:,0]
    
    if (nr_iter > max_nr_iters):
        raise Exception('findorbit6 did not converge!')
    
    if refpts is None:
        return co[:,0]
    
    try:
        refpts[0]
    except:
        refpts = [refpts]
        
    orb = tracking.linepass(line = ring, particles = numpy.array(co), refpts = range(len(ring)+1), engine = engine)
    return orb[:,refpts]  
    
    
def calcm66 (line, m66_list = None, closed_orbit = None):
    """ returns the total transfer matrix (or one-turn matrix) """
    if m66_list is None:
        m66_list, closed_orbit = tracking.findm66(line = line, closed_orbit = closed_orbit)
    m = numpy.eye(6,6)
    for i in range(m66_list.shape[0]):
        m = numpy.dot(m66_list[i,:,:], m)
    return (m, m66_list, closed_orbit)

def fractunes(ring, m66 = None, m66_list = None, closed_orbit = None):
    """ returns uncoupled fractional tunes """
    if closed_orbit is None:
        closed_orbit = findorbit6(ring, range(len(ring)))
    if m66 is None:
        m66,m66_list,closed_orbit = calcm66(ring, m66_list = m66_list, closed_orbit = closed_orbit)
    nux = math.acos((m66[0,0]+m66[1,1])/2)/(2*math.pi)
    nuy = math.acos((m66[2,2]+m66[3,3])/2)/(2*math.pi)
    nus = math.acos((m66[4,4]+m66[5,5])/2)/(2*math.pi)
    return ((nux,nuy,nus), m66, m66_list, closed_orbit)

def fractunes_coupled(ring, m66 = None, m66_list = None, closed_orbit = None):
    """ returns coupled fractional tunes """
    raise Exception('fractunes_coupled: not yet implemented')


def twiss (line, refpts = None, m66 = None, m66_list = None, closed_orbit = None, twiss_in = None):
    """ returns uncoupled Twiss parameters """
    
    ''' process arguments '''
    if refpts is None:
        refpts = range(len(line))
    try:
        refpts[0]
    except:
        refpts = [refpts]
    if m66 is None:
        m66,m66_list,closed_orbit = calcm66(line, m66_list = m66_list, closed_orbit = closed_orbit)
    if twiss_in is None:
        twiss_in = Twiss()
        twiss_in.closed_orbit = closed_orbit
        (twiss_in.mux, twiss_in.muy) = (0,0)
    
    
    
    ''' calcs twiss at first element '''
    (mx, my) = (m66[0:2,0:2], m66[2:4,2:4]) # decoupled transfer matrices
    sin_nux = math.copysign(1,mx[0,1]) * math.sqrt(-mx[0,1] * mx[1,0] - ((mx[0,0] - mx[1,1])**2)/4);
    sin_nuy = math.copysign(1,my[0,1]) * math.sqrt(-my[0,1] * my[1,0] - ((my[0,0] - my[1,1])**2)/4);
    t = Twiss()
    t.alphax  = (mx[0,0] - mx[1,1]) / 2 / sin_nux
    t.betax   = mx[0,1] / sin_nux
    t.alphay  = (my[0,0] - my[1,1]) / 2 / sin_nuy
    t.betay   = my[0,1] / sin_nuy
    ''' dispersion function based on eta = (1 - M)^(-1) D'''
    Dx = numpy.array([[m66[0,4]],[m66[1,4]]])
    Dy = numpy.array([[m66[2,4]],[m66[3,4]]]) 
    t.etax = numpy.linalg.solve(numpy.eye(2,2) - mx, Dx)
    t.etay = numpy.linalg.solve(numpy.eye(2,2) - my, Dy)
    
    if 0 in refpts:
        tw = [t]
    else:
        tw = []
        
    ''' propagates twiss through line '''
    for i in range(1,1+len(line)):
        m = m66_list[i-1,:,:]
        (mx, my) = (m[0:2,0:2], m[2:4,2:4]) # decoupled transfer matrices
        Dx = numpy.array([[m[0,4]],[m[1,4]]])
        Dy = numpy.array([[m[2,4]],[m[3,4]]])
        n = Twiss()
        n.betax  =  ((mx[0,0] * t.betax - mx[0,1] * t.alphax)**2 + mx[0,1]**2) / t.betax
        n.alphax = -((mx[0,0] * t.betax - mx[0,1] * t.alphax) * (mx[1,0] * t.betax - mx[1,1] * t.alphax) + mx[0,1] * mx[1,1]) / t.betax
        n.betay  =  ((my[0,0] * t.betay - my[0,1] * t.alphay)**2 + my[0,1]**2) / t.betay
        n.alphay = -((my[0,0] * t.betay - my[0,1] * t.alphay) * (my[1,0] * t.betay - my[1,1] * t.alphay) + my[0,1] * my[1,1]) / t.betay
        ''' calcs phase advance based on R(mu) = U(2) M(2|1) U^-1(1) '''
        n.mux    = t.mux + math.asin(mx[0,1]/math.sqrt(n.betax * t.betax)) 
        n.muy    = t.muy + math.asin(my[0,1]/math.sqrt(n.betay * t.betay))
        ''' dispersion function '''
        n.etax = Dx + numpy.dot(mx, t.etax)
        n.etay = Dy + numpy.dot(my, t.etay)
    
        if i in refpts:
            tw.append(n)
        t = copy.deepcopy(n)
    
    ''' converts eta format '''
    for t in tw:
        (t.etaxl, t.etayl) = (t.etax[1,0], t.etay[1,0])
        (t.etax,  t.etay ) = (t.etax[0,0], t.etay[0,0])
        
    return (tw, m66, m66_list, closed_orbit)
    
    
def twiss_coupled (line, refpts = None, m66 = None, m66_list = None, closed_orbit = None, twiss_in = None):
    """ returns coupled Twiss parameters """
    raise Exception('twiss_coupled: not yet implemented')
    