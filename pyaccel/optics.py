import pyaccel.lattice as _lattice
import mathphys as _mp

class OpticsException(Exception):
    pass

def get_rfrequency(lattice):
    try:
        lattice = lattice.lattice
    except:
        pass
    for element in lattice:
        try:
            return element.frequency
        except:
            pass
    raise OpticsException('No cavity element in the lattice')

def get_revolution_period(accelerator):
    _,velocity,_,_ = _mp.beam_optics.calc_brho(energy = accelerator.energy / 1e9)
    circumference = _lattice.lengthlatt(accelerator.lattice)
    return circumference/velocity

def get_revolution_frequency(accelerator):
    return 1.0 / get_revolution_period(accelerator)

def get_fractunes(lattice):
    raise OpticsException('not implemented')

def get_tunes(lattice):
    raise OpticsException('not implemented')

def get_chromaticities(lattice):
    raise OpticsException('not implemented')

def get_mcf(lattice):
    raise OpticsException('not implemented')

def get_radiation_integrals(accelerator):
    raise OpticsException('not implemented')
