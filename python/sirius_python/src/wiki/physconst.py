
import math


light_speed              = 299792458                                            # [m/s]   - definition
vacuum_permeability      = 4*math.pi*1e-7                                       # [T.m/A] - definition
electron_charge          = 1.60217656535e-19                                    # [C]     - 2014-06-11
electron_mass            = 9.1093829140e-31                                     # [Kg]    - 2014-06-11
reduced_planck_constant  = 6.5821192815e-16                                     # [eV.s]  - 2014-07-22
electron_rest_energy     = electron_mass * math.pow(light_speed,2)              # [Kg.m^2/s^2] - derived
vacuum_permitticity      = 1.0/(vacuum_permeability * math.pow(light_speed,2))  # [V.s/(A.m)]  - derived
electron_rest_energy_MeV = (electron_rest_energy / electron_charge) / 1e6       # [MeV] - derived
electron_radius          = math.pow(electron_charge,2)/(4*math.pi*vacuum_permitticity*electron_rest_energy)                      # [m] - derived
rad_cgamma               = 4*math.pi*electron_radius/math.pow(electron_rest_energy/electron_charge/1e9,3)/3                      # [m]/[GeV]^3 - derived
Cq                       = (55.0/(32*math.sqrt(3.0))) * reduced_planck_constant * light_speed / (1e6 * electron_rest_energy_MeV) # [m] - derived
