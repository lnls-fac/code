import pyaccel as _pyaccel
from . import _lattice

_default_radiation_on = False
_default_cavity_on    = False
_default_vchamber_on  = False
_version              = 'SI_V07'

def create_accelerator(cavity_on=_default_cavity_on,
                       radiation_on=_default_radiation_on,
                       vchamber_on=_default_vchamber_on,
                       energy=_lattice._energy,
                       harmonic_number=_lattice._harmonic_number):

    accelerator = _pyaccel.accelerator.Accelerator()
    accelerator.lattice = _lattice.create_lattice()

    # global tracking parameters
    accelerator.cavity_on       = cavity_on
    accelerator.radiation_on    = radiation_on
    accelerator.vchamber_on     = vchamber_on
    accelerator.energy          = energy
    accelerator.harmonic_number = harmonic_number
    accelerator.version         = _version
    accelerator.mode            = _lattice._default_optics_mode.mode

    return accelerator
