import pyaccel as _pyaccel
from . import _lattice

_energy = 3.0e9 # [eV]
_harmonic_number = 864
_default_cavity_on = False
_default_radiation_on = False
_default_vchamber_on = False

def create_accelerator():

        the_ring = _lattice.create_lattice()
        accelerator = _pyaccel.accelerator.Accelerator(
            elements=the_ring,
            energy=_energy,
            harmonic_number=_harmonic_number,
            cavity_on=_default_cavity_on,
            radiation_on=_default_radiation_on,
            vchamber_on=_default_vchamber_on)

        return accelerator
