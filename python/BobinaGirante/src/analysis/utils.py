import math
import mathphysicslibs

def calc_beta_gamma(energy):
    c = mathphysicslibs.constants
    gamma = energy / (c.electron_rest_energy/1000)
    beta  = math.sqrt(1.0 - 1.0/gamma**2)
    brho  = 1e9 * (beta * energy / c.light_speed)
    return (beta,gamma,brho) 
    