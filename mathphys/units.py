# International System of Units
# =============================
# ref.: http://en.wikipedia.org/wiki/Si_system

from mathphys.base_units import *
import mathphys.constants

# Derived units
# =============
newton  = kilogram * meter / second
joule   = newton * meter
watt    = joule / second
coulomb = second * ampere
volt    = watt / ampere
weber   = volt * second
tesla   = weber / meter**2

radian                  = (meter / meter)
(km,cm,mm,um,nm)        = (1e3,1e-2,1e-3,1e-6,1e-9)
(rad,mrad,urad,nrad)    = (1e0,1e-3,1e-6,1e-9)
(minutes,hour,day,year) = (60,60*60,24*60*60,365.25*24*60*60)

electron_volt           = mathphys.constants.elementary_charge * volt
(eV,MeV,GeV)            = (electron_volt,electron_volt*1e6,electron_volt*1e9)

# conversions
# ============
meter_2_mm = (meter / mm)
mm_2_meter = (mm / meter)
mrad_2_rad = (mrad / rad)
rad_2_mrad = (rad / mrad)

def kelvin_2_celsius(k): return k - 273.15
def joule_2_eV(e): return e / electron_volt
def radian_2_degree(r): return (180.0/math.pi) * r