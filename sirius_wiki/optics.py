# -*- coding: utf-8 -*-

import math
import mathphys.constants as const
import mathphys.units as units

def gamma(energy):
    '''Gamma from energy[GeV].'''
    return energy * 1.0e9 / units.joule_2_eV(const.electron_rest_energy)
    
def beta(gamma):
    '''Beta factor from gamma.'''
    return math.sqrt(((gamma + 1.0)/gamma)*((gamma - 1.0)/gamma))
  
def velocity(beta):
    '''Velocity [m/s] from ebeam beta factor.'''
    return beta * const.light_speed

def brho(energy, beta):
    '''Magnetic rigidity [T.m] from ebeam energy [GeV] and beta factor.'''
    return beta * (energy * 1e9) / const.light_speed

def rho(brho, field):
    '''Bending radius [m] from magnetic rigidity [T.m].'''
    return brho / field

def critical_energy(gamma, rho):
    '''Critical energy [keV] from ebeam gamma factor and bending radius [m].'''
    return (3 * units.joule_2_eV(const.reduced_planck_constant) * const.light_speed *
            math.pow(gamma, 3)/ (2.0 * rho)) / 1000

def U0(energy, I2):
    '''Energy loss U0 [keV] from ebeam energy [GeV] and I2[1/m].'''
    return 1e6 * const.rad_cgamma * math.pow(energy, 4) * I2 / 2.0 / math.pi

def sync_phase(q):
    '''Synchronous phase [deg] from overvoltage.'''
    return 180.0 - math.degrees(math.asin(1.0/q))

def rf_energy_acceptance(q, energy, U0, h, alpha):
    '''RF energy acceptance [%] from overvoltage, ebeam energy [GeV], energy
       loss U0 per turn [keV], harmonic number h and linear compaction factor
       alpha.'''
    Fq = 0.0
    if q > 1.0:
        Fq = 2.0*(math.sqrt(q*q-1.0) - math.acos(1.0/q))
    energy_accpt = (math.sqrt((1.0/math.pi/alpha/h) * (U0/(energy*1e6))*Fq))
    return 100 * energy_accpt

def natural_emittance(gamma, Jx, I2, I5):
    '''Natural emittance [nm·rad] from ebeam gamma factor, damping partition
       number Jx, I2[1/m] and I5 [1/m].'''
    emitt = const.Cq * gamma*gamma*I5/(Jx*I2) * 1e9
    return emitt

def energy_spread(gamma, I2, I3, I4):
    '''Natural energy spread from ebeam gamma factor, I2[1/m], I3[1/m^2] and
    I4[1/m].'''
    sigmae = math.sqrt(const.Cq * gamma * gamma * I3 / (2*I2 + I4))
    return 100 * sigmae

def revolution_period(circumference, velocity):
    '''Revolution period [μs] from circumference [m] and velocity [m/s].'''
    return 1.0e6 * circumference / velocity

def revolution_frequency(revolution_period):
    '''Revolution frequency [MHz] from revolution period [μs].'''
    return 1.0 / revolution_period

def rf_frequency(revolution_frequency, harmonic_number):
    '''RF frequency [MHz] from revolution frequency [MHz] and harmonic
       number.'''
    return revolution_frequency * harmonic_number

def number_of_electrons(current, revolution_period):
    '''Number of electrons from beam current [mA] and revolution
       period [μs].'''
    return (current/1e3) * (revolution_period/1e6) / const.elementary_charge

def overvoltage(rf_voltage, U0):
    '''Overvoltage from RF voltage [MV] and energy loss U0 per turn [keV].'''
    return 1e6*rf_voltage / (1e3*U0)

def alpha1(I1, circumference):
    '''Linear momentum compaction factor from I1 [m] and circumference [m].'''
    return I1 / circumference

def Jx(I2, I4):
    '''Horizontal damping partition number from I2 [1/m] and I4 [1/m].'''
    return 1 - I4/I2

def Js(Jx, Jy):
    '''Longitudinal damping partition number from Jx and Jy.'''
    return 4.0 - Jx - Jy

def frequency_from_tune(revolution_frequency, tune):
    '''Frequency [kHz] from revolution frequency [MHz] and tune.'''
    return 1000*revolution_frequency*(tune - math.floor(tune))

def damping_time(energy, I2, J, circumference):
    '''Radiation damping time [ms] from beam energy [GeV], radiation
       integral I2 [1/m], damping partition number and circumference [m].'''
    return 1000 * circumference / (const.Ca*math.pow(energy, 3)*I2*J)

def radiation_power(current, U0):
    '''Radiation power [kW] from beam current [mA] and
       energy loss per turn [keV].'''
    return U0 * current / 1000

def rf_wavelength(frequency):
    '''RF wavelength [m] from RF frequency [MHz].'''
    return const.light_speed / (1e6*frequency)

def slip_factor(alpha, gamma):
    '''Slip factor from momentum compaction factor alpha and gamma.'''
    return alpha - 1/math.pow(gamma, 2)

def bunch_length(slip_factor, energy_spread, synchrotron_frequency):
    '''Natural bunch length [mm] from slip factor, natural energy spread [%],
       synchrotron frequency [kHz].'''
    angular_synchrotron_frequency = 2 * math.pi * synchrotron_frequency
    return (const.light_speed * abs(slip_factor) * energy_spread/100 /
            (1e3*angular_synchrotron_frequency)) * 1000

def bunch_duration(bunch_length, beta):
    '''Bunch lenth in time units [ps] from bunch length [mm] and beta
       factor.'''
    return 1e9 * bunch_length / beta / const.light_speed

def id_deflection_parameter(field, period):
    '''insertion device deflection parameter from field [T] and period [mm]'''
    return 1e-9 * period * field * const.light_speed / (units.joule_2_eV(const.electron_rest_energy)/1.0e6) / (2*math.pi)

def id_mean_power(energy, current, period, nr_periods, k):
    '''insertion device mean power from beam energy [GeV], current [mA], ID period [mm], ID nr periods and k
       see Handbook of Acc. Physics, eq.(14), pg 189'''
    cst = math.pi * 1e9 * const.rad_cgamma * (units.joule_2_eV(const.electron_rest_energy)/1.0e9)**2
    return (cst * energy * k**2 * nr_periods / (period/1000.0))/1000.0
    
