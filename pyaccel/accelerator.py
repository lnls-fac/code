
import trackcpp as _trackcpp
import pyaccel.lattice


class Accelerator(object):

    def __init__(self, lattice, energy=0.0, harmonic_number=0):
        if isinstance(lattice, list):
            lattice = pyaccel.lattice.Lattice(lattice)
        self._a = _trackcpp.Accelerator()
        self._a.lattice = lattice._lattice
        self.energy = energy
        self.harmonic_number = harmonic_number

    @property
    def energy(self):
        return self._a.energy

    @energy.setter
    def energy(self, value):
        self._a.energy = value

    @property
    def harmonic_number(self):
        return self._a.harmonic_number

    @harmonic_number.setter
    def harmonic_number(self, value):
        return self._a.harmonic_number

    @property
    def cavity_on(self):
        return self._a.cavity_on

    @cavity_on.setter
    def cavity_on(self, value):
        self._a.cavity_on = value

    @property
    def radiation_on(self):
        return self._a.radiation_on

    @radiation_on.setter
    def radiation_on(self, value):
        self._a.radiation_on = value

    @property
    def vchamber_on(self):
        return self._a.vchamber_on

    @vchamber_on.setter
    def vchamber_on(self, value):
        self._a.vchamber_on = value

    @property
    def lattice(self):
        return pyaccel.lattice.Lattice(lattice=self._a.lattice)

    @lattice.setter
    def lattice(self, value):
        if not isinstance(value, pyaccel.lattice.Lattice):
            raise TypeError('value must be Lattice')
        self._a.lattice = value._lattice
