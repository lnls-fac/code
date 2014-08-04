
import math
import physconst as const


def gamma(energy):
    '''Gamma from energy[GeV]''' 
    return energy * 1000 / const.electron_rest_energy_MeV
    
def beta(gamma):
    '''Beta factor from gamma'''
    return ((gamma + 1.0)/gamma)*((gamma - 1.0)/gamma)
  
def velocity(beta):
    '''Velocity [m/s] from ebeam beta factor'''
    return beta * const.light_speed

def brho(energy, beta):
    '''Magnetic rigidity [T.m] from ebeam energy [GeV] and beta factor''' 
    return beta * (energy * 1e9) / const.light_speed

def critical_energy(energy, field):
    '''Critical energy [keV] from ebeam energy [GeV] and magnetic field [T]''' 
    gamma = gamma(energy)
    beta  = beta(gamma)
    brho  = brho(energy, beta)
    rho   = brho / field 
    cenergy = (3 * const.reduced_planck_constant * const.light_speed * math.pow(gamma, 3)/ (2.0 * rho)) / 1000
    return cenergy


def U0(energy, I2):
    '''Energy loss U0 [keV] from ebeam energy [GeV] and I2[1/m]'''
    return 1e6 * const.rad_cgamma * math.pow(energy, 4) * I2 / 2.0 / math.pi

def sync_phase(q):
    '''Synchronous phase [deg] from overvoltage'''
    return 180.0 - (180.0/math.pi) * math.asin(1.0/q)

def rf_energy_acceptance(q, energy, U0, h, alpha):
    '''RF energy acceptance [%] from overvoltage, ebeam energy [GeV], energy loss U0 per turn [keV], 
    harmonic number h and linear compaction factor alpha'''
    Fq = 0.0
    if q > 1.0:
        Fq = 2.0*(math.sqrt(q*q-1.0) - math.acos(1.0/q))
    energy_accpt = math.sqrt((1.0 / math.pi / alpha / h) * (U0 / (energy * 1e6)) * Fq) 
    return 100 * energy_accpt

def natural_emittance(gamma, Jx, I2, I5):
    '''Natural emittance [nm.rad] from ebeam gamma factor, damping partition number Jx, I2[1/m] and I5 [1/m]'''
    emitt = const.Cq * gamma*gamma*I5/(Jx*I2) * 1e9
    return emitt

def energy_spread(gamma, I2, I3, I4):
    '''Natural energy spread from ebeam gamma factor, I2[1/m], I3[1/m^2] and I4[1/m]'''
    sigmae = math.sqrt(const.Cq * gamma * gamma * I3 / (2*I2 + I4))
    return 100 * sigmae

