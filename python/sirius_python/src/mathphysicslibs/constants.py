import math

# International System of Units
# =============================
# ref.: http://en.wikipedia.org/wiki/Si_system


# Base Units
# ----------
second   = 1.0
meter    = 1.0
kilogram = 1.0
ampere   = 1.0
kelvin   = 1.0
mole     = 1.0
candela  = 1.0

# Derived units
# -------------
newton  = kilogram * meter / second
joule   = newton * meter
watt    = joule / second
coulomb = second * ampere
volt    = watt / ampere
weber   = volt * second
tesla   = weber / meter**2

# defined physical constants
# ==========================

light_speed          = 299792458 * (meter/second)

# Physical constants
# ------------------

elementary_charge    = 1.60217656535e-19 * coulomb
electron_volt        = elementary_charge * volt
(eV,MeV,GeV)         = (electron_volt,electron_volt*1e6,electron_volt*1e9)
electron_rest_mass   = 9.1093821545e-31 * kilogram
electron_rest_energy = 0.51099891013 * MeV

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


