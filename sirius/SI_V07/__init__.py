from . import _lattice
create_lattice = _lattice.create_lattice

# -- default accelerator values for SI_V07 --

energy = _lattice._energy
harmonic_number = _lattice._harmonic_number
default_cavity_state_on = False
default_cavity_radiation_on = False
default_optics_mode = _lattice._default_optics_mode
