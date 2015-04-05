import math as _math
import mathphys as _mp

class Beam:

    def __init__(self, energy, current = 0):

        self.energy = energy
        self.current = current
        self.brho, self.velocity, self.beta, self.gamma = Beam.calc_brho(self.energy)

    @staticmethod
    def calc_brho(energy = None, gamma = None, beta = None, velocity = None):
        electron_rest_energy_GeV = mathphys.units.joule_2_eV(mathphys.constants.electron_rest_energy) / 1e9
        gamma    = energy/electron_rest_energy_GeV
        beta     = math.sqrt(((gamma-1.0)/gamma)*((gamma+1.0)/gamma))
        velocity = mathphys.constants.light_speed * beta
        brho     = beta * (energy * 1e9) / mathphys.constants.light_speed
        return brho, velocity, beta, gamma

    def __str__(self):
        r = ''
        r += '{0:<10s} {1:f} GeV'.format('energy:', self.energy)
        r += '\n{0:<10s} {1:f}'.format('gamma:', self.gamma)
        r += '\n{0:<10s} 1 - {1:e}'.format('beta:', 1.0-self.beta)
        r += '\n{0:<10s} {1:.0f} - {2:f} m/s'.format('velocity:', consts.light_speed, consts.light_speed - self.velocity)
        r += '\n{0:<10s} {1:f} T.m'.format('brho:', self.brho)
        return r


def beam_rigidity(**kwargs):

    electron_rest_energy_eV = _mp.units.joule_2_eV(_mp.constants.electron_rest_energy)

    if len(kwargs) != 1:
        raise Exception('beam rigidity accepts only one argument')

    if 'brho' in kwargs:
        k = kwargs['brho'] / (electron_rest_energy_eV/_mp.constants.light_speed)
        kwargs['gamma'] = _math.sqrt(1.0+k**2)
    if 'velocity' in kwargs:
        kwargs['beta'] = kwargs['velocity'] / _mp.constants.light_speed
    if 'beta' in kwargs:
        kwargs['gamma'] = 1.0/_math.sqrt(1.0 - kwargs['beta']**2)
    if 'gamma' in kwargs:
        kwargs['energy'] = kwargs['gamma'] * electron_rest_energy_GeV

    energy = kwargs['energy']
    gamma = kwargs['gamma'] if 'gamma' in kwargs else energy/electron_rest_energy_eV
    beta = kwargs['beta'] if 'beta' in kwargs else _math.sqrt(((gamma-1.0)/gamma)*((gamma+1.0)/gamma))
    velocity = kwargs['velocity'] if 'velocity' in kwargs else _mp.constants.light_speed * beta
    brho = kwargs['brho'] if 'brho' in kwargs else beta * (energy) / _mp.constants.light_speed

    return brho, velocity, beta, gamma, energy
