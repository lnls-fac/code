import pyaccel.lattice as _lattice
import pyaccel.tracking as _tracking
import mathphys as _mp
import math as _math
import numpy as _np
import copy as _copy

class OpticsException(Exception):
    pass

class Twiss:
    def __init__(self):
        self.closed_orbit = _np.zeros((6,1))
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

def gettwiss(twiss_list, attributes_list):
    """Build a matrix with Twiss data from a list of Twiss objects.

    Accepts a list of Twiss objects and returns a matrix with Twiss data, one line for
    each Twiss parameter defined in 'attributes_list'.

    Keyword arguments:
    twiss_list -- List with Twiss objects
    attributes_list -- List of strings with Twiss attributes to be stored in twiss matrix

    Returns:
     -- Matrix with Twiss data
    """
    values = _np.zeros((len(attributes),len(twiss_list)))
    for i in range(len(twiss_list)):
        for j in range(len(attributes_list)):
            values[j,i] = getattr(twiss_list[i], attributes_list[j])
    return values

def twiss (accelerator = None,
           refpts = None,
           transfer_matrices = None,
           closed_orbit = None,
           twiss_in = None):

    """ returns uncoupled Twiss parameters """

    ''' process arguments '''
    if refpts is None:
        refpts = range(len(accelerator))

    try:
        refpts[0]
    except:
        refpts = [refpts]

    if transfer_matrices is None:
        transfer_matrices = _tracking.findm66(accelerator = accelerator, closed_orbit = closed_orbit)
    if twiss_in is None:
        twiss_in = Twiss()
        twiss_in.closed_orbit = closed_orbit
        twiss_in.mux, twiss_in.muy = 0, 0

    m66 = transfer_matrices[-1]

    ''' calcs twiss at first element '''
    mx, my = m66[0:2,0:2], m66[2:4,2:4] # decoupled transfer matrices
    sin_nux = _math.copysign(1,mx[0,1]) * _math.sqrt(-mx[0,1] * mx[1,0] - ((mx[0,0] - mx[1,1])**2)/4);
    sin_nuy = _math.copysign(1,my[0,1]) * _math.sqrt(-my[0,1] * my[1,0] - ((my[0,0] - my[1,1])**2)/4);
    t = Twiss()
    t.alphax  = (mx[0,0] - mx[1,1]) / 2 / sin_nux
    t.betax   = mx[0,1] / sin_nux
    t.alphay  = (my[0,0] - my[1,1]) / 2 / sin_nuy
    t.betay   = my[0,1] / sin_nuy
    ''' dispersion function based on eta = (1 - M)^(-1) D'''
    Dx = _np.array([[m66[0,4]],[m66[1,4]]])
    Dy = _np.array([[m66[2,4]],[m66[3,4]]])
    t.etax = _np.linalg.solve(_np.eye(2,2) - mx, Dx)
    t.etay = _np.linalg.solve(_np.eye(2,2) - my, Dy)

    if 0 in refpts:
        tw = [t]
    else:
        tw = []

    ''' propagates twiss through line '''
    m_previous = _np.eye(6,6)
    for i in range(len(accelerator)):
        m_current = transfer_matrices[i-1]
        m = _np.dot(m_current, _np.linalg.inv(m_previous))
        m_previous = m_current
        mx, my = m[0:2,0:2], m[2:4,2:4] # decoupled transfer matrices
        Dx = _np.array([[m[0,4]],[m[1,4]]])
        Dy = _np.array([[m[2,4]],[m[3,4]]])
        n = Twiss()
        n.betax  =  ((mx[0,0] * t.betax - mx[0,1] * t.alphax)**2 + mx[0,1]**2) / t.betax
        n.alphax = -((mx[0,0] * t.betax - mx[0,1] * t.alphax) * (mx[1,0] * t.betax - mx[1,1] * t.alphax) + mx[0,1] * mx[1,1]) / t.betax
        n.betay  =  ((my[0,0] * t.betay - my[0,1] * t.alphay)**2 + my[0,1]**2) / t.betay
        n.alphay = -((my[0,0] * t.betay - my[0,1] * t.alphay) * (my[1,0] * t.betay - my[1,1] * t.alphay) + my[0,1] * my[1,1]) / t.betay
        ''' calcs phase advance based on R(mu) = U(2) M(2|1) U^-1(1) '''
        n.mux    = t.mux + _math.asin(mx[0,1]/_math.sqrt(n.betax * t.betax))
        n.muy    = t.muy + _math.asin(my[0,1]/_math.sqrt(n.betay * t.betay))
        ''' dispersion function '''
        n.etax = Dx + _np.dot(mx, t.etax)
        n.etay = Dy + _np.dot(my, t.etay)

        if i in refpts:
            tw.append(n)
        t = _copy.deepcopy(n)

    ''' converts eta format '''
    for t in tw:
        t.etaxl, t.etayl = (t.etax[1,0], t.etay[1,0])
        t.etax,  t.etay  = (t.etax[0,0], t.etay[0,0])

    return tw

def get_rfrequency(lattice):
    try:
        lattice = lattice.lattice
    except:
        pass
    for element in lattice:
        try:
            return element.frequency
        except:
            pass
    raise OpticsException('No cavity element in the lattice')

def get_revolution_period(accelerator):
    _,velocity,_,_ = _mp.beam_optics.calc_brho(energy = accelerator.energy / 1e9)
    circumference = _lattice.lengthlatt(accelerator.lattice)
    return circumference/velocity

def get_revolution_frequency(accelerator):
    return 1.0 / get_revolution_period(accelerator)

def get_fractunes(lattice):
    raise OpticsException('not implemented')

def get_tunes(lattice):
    raise OpticsException('not implemented')

def get_chromaticities(lattice):
    raise OpticsException('not implemented')

def get_mcf(lattice):
    raise OpticsException('not implemented')

def get_radiation_integrals(accelerator):
    raise OpticsException('not implemented')
