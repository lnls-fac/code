import math

# International System of Units
# =============================
# ref.: http://en.wikipedia.org/wiki/Si_system

# Base Units
# ==========
second   = 1.0
meter    = 1.0
kilogram = 1.0
ampere   = 1.0
kelvin   = 1.0
mole     = 1.0
candela  = 1.0

# Derived units
# =============
newton  = kilogram * meter / second
joule   = newton * meter
watt    = joule / second
coulomb = second * ampere
volt    = watt / ampere
weber   = volt * second
tesla   = weber / meter**2

# defined physical constants
# ==========================

light_speed              = 299792458 * (meter/second)                                            # [m/s]   - definition
vacuum_permeability      = 4*math.pi*1e-7 * (volt * second / ampere / meter)                                      # [T.m/A] - definition
elementary_charge        = 1.60217656535e-19 * coulomb
electron_mass            = 9.1093829140e-31 * kilogram                                    # [Kg]    - 2014-06-11
reduced_planck_constant  = 6.5821192815e-16                                      # [eV.s]  - 2014-07-22
electron_rest_energy     = electron_mass * math.pow(light_speed,2)              # [Kg.m^2/s^2] - derived
vacuum_permitticity      = 1.0/(vacuum_permeability * math.pow(light_speed,2))  # [V.s/(A.m)]  - derived
electron_rest_energy_MeV = (electron_rest_energy / elementary_charge) / 1e6       # [MeV] - derived
electron_radius          = math.pow(elementary_charge,2)/(4*math.pi*vacuum_permitticity*electron_rest_energy)                      # [m] - derived
rad_cgamma               = 4*math.pi*electron_radius/math.pow(electron_rest_energy/elementary_charge/1e9,3)/3                      # [m]/[GeV]^3 - derived
Cq                       = (55.0/(32*math.sqrt(3.0))) * reduced_planck_constant * light_speed / (1e6 * electron_rest_energy_MeV) # [m] - derived
Ca                       = electron_radius*light_speed / (3*math.pow(electron_rest_energy_MeV/1000, 3))                          # [m^2/(s.GeV^3)] - derived
 
# Physical constants
# ==================

electron_volt        = elementary_charge * volt
(eV,MeV,GeV)         = (electron_volt,electron_volt*1e6,electron_volt*1e9)

def to_celsius(k): return k - 273.15
def to_eV(e): return e / electron_volt
def to_deg(g): return (180/math.pi) * g

radian                  = (meter / meter)
(km,cm,mm,um,nm)        = (1e3,1e-2,1e-3,1e-6,1e-9)
(rad,mrad,urad,nrad)    = (1e0,1e-3,1e-6,1e-9)
(minutes,hour,day,year) = (60,60*60,24*60*60,365.25*24*60*60)

# conversions
# ============

meter_2_mm = (mm / meter)
mm_2_meter = (meter / mm)
mrad_2_rad = (rad / mrad)
rad_2_mrad = (mrad / rad)

