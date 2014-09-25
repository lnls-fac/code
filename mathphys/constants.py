import math
import mathphys.base_units as u

# temporary auxiliary derived units
u.volt    = (u.kilogram * u.meter**2) / (u.ampere * u.second**2)
u.coulomb = u.second * u.ampere

# physical constants
# ==================
light_speed              = 299792458 * (u.meter/u.second)                            # [m/s]   - definition
vacuum_permeability      = 4*math.pi*1e-7 * (u.volt * u.second / u.ampere / u.meter) # [T.m/A] - definition
elementary_charge        = 1.60217656535e-19 * (u.coulomb)                           # [C]     - 2014-06-11
electron_mass            = 9.1093829140e-31 * u.kilogram                             # [Kg]    - 2014-06-11
electron_rest_energy     = electron_mass * math.pow(light_speed,2)                   # [Kg.m^2/s^2] - derived
vacuum_permitticity      = 1.0/(vacuum_permeability * math.pow(light_speed,2))       # [V.s/(A.m)]  - derived
electron_rest_energy_MeV = (electron_rest_energy / elementary_charge) / 1e6          # [MeV] - derived
reduced_planck_constant  = 6.5821192815e-16                                          # [eV.s]  - 2014-07-22
electron_radius          = math.pow(elementary_charge,2)/(4*math.pi*vacuum_permitticity*electron_rest_energy)                      # [m] - derived
rad_cgamma               = 4*math.pi*electron_radius/math.pow(electron_rest_energy/elementary_charge/1e9,3)/3                      # [m]/[GeV]^3 - derived
Cq                       = (55.0/(32*math.sqrt(3.0))) * reduced_planck_constant * light_speed / (1e6 * electron_rest_energy_MeV) # [m] - derived
Ca                       = electron_radius*light_speed / (3*math.pow(electron_rest_energy_MeV/1000, 3))                          # [m^2/(s.GeV^3)] - derived

del u  # cleans up namespace