
import trackcpp as _trackcpp
import lattice


class Accelerator:

    def __init__(
            self,
            energy,
            cavity_on=False,
            radiation_on=False,
            vchamber_on=False,
            harmonic_number=1,
            lattice=[],
            kicktables=[]):
        self.energy = energy
        self.cavity_on = cavity_on
        self.radiation_on = radiation_on
        self.vchamber_on = vchamber_on
        self.harmonic_number = harmonic_number

