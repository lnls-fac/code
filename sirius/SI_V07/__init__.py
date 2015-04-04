from . import _lattice

create_lattice = _lattice.create_lattice

# -- default accelerator values for SI_V07 --

energy = 3.0 # [GeV]
harmonic_number = 864
default_cavity_state_on = False
default_cavity_radiation_on = False
default_optics_mode = _lattice._default_optics_mode
