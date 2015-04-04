
import trackcpp as _trackcpp
import pyaccel.lattice

class AcceleratorException(Exception):
    pass

class Accelerator(object):

    def __init__(self, **kwargs):

        if 'accelerator' in kwargs:
            a = kwargs['accelerator']
            if isinstance(a,_trackcpp.Accelerator):
                self._accelerator = a
            else:
                self._accelerator = kwargs['accelerator']._accelerator
        else:
            self._accelerator = _trackcpp.Accelerator()
            self._accelerator.cavity_on = False
            self._accelerator.radiation_on = False
            self._accelerator.vchamber_on = False
            self._accelerator.harmonic_number = 0

        if 'elements' in kwargs:
            elements = kwargs['elements']
            if isinstance(elements, _trackcpp.CppElementVector):
                self._accelerator.lattice = elements
            elif isinstance(elements, list):
                for e in elements:
                    self._accelerator.lattice.append(e._e)
                #self._accelerator.lattice = _trackcpp.CppElementVector(elements)
            else:
                raise TypeError('values must be list of Element')

        if 'energy' in kwargs:
            self._accelerator.energy = kwargs['energy']
        if 'harmonic_number' in kwargs:
            self._accelerator.harmonic_number = kwargs['harmonic_number']
        if 'radiation_on' in kwargs:
            self._accelerator.radiation_on = kwargs['radiation_on']
        if 'cavity_on' in kwargs:
            self._accelerator.cavity_on = kwargs['cavity_on']
        if 'vchamber_on' in kwargs:
            self._accelerator.vchamber_on = kwargs['vchamber_on']

    def __getitem__(self, index):

        if isinstance(index,int):
            return pyaccel.elements.Element(element=self._accelerator.lattice[index])
        elif isinstance(index, (list,tuple)):
            lattice = _trackcpp.CppElementVector()
            for i in index:
                lattice.append(self._accelerator.lattice[i])
        elif isinstance(index, slice):
            lattice = self._accelerator.lattice[index]
        else:
            raise TypeError('invalid index')
        a = Accelerator(
                elements=lattice,
                energy=self._accelerator.energy,
                harmonic_number=self._accelerator.harmonic_number,
                cavity_on=self._accelerator.cavity_on,
                radiation_on=self._accelerator.radiation_on,
                vchamber_on=self._accelerator.vchamber_on)
        return a

    def __setitem__(self, index, value):

        if isinstance(index,int):
            self._accelerator.lattice[index] = value._e
        elif isinstance(index, (list, tuple)):
            if isinstance(value, (list,tuple)):
                for i in range(len(value)):
                    v = value[i]
                    if not isinstance(v, pyaccel.elements.Element):
                        raise TypeError('invalid value')
                    self._accelerator.lattice[index[i]] = v._e
            else:
                if not isinstance(value, pyaccel.elements.Element):
                    raise TypeError('invalid value')
                for i in range(len(value)):
                    self._accelerator.lattice[index[i]] = value._e
        elif isinstance(index, slice):
            start, stop, step = index.indices(len(self._accelerator.lattice))
            iterator = range(start, stop, step)
            if isinstance(value, (list, tuple)):
                for i in iterator:
                    print(i,self._accelerator.lattice[i],value[i])
                    self._accelerator.lattice[i] = value[i]._e
            else:
                for i in iterator:
                    self._accelerator.lattice[i] = value._e

    def __len__(self):
        return len(self._accelerator.lattice)

    def append(self, value):
        if not isinstance(value, pyaccel.elements.Element):
            raise TypeError('value must be Element')
        self._accelerator.lattice.append(value._e)

    @property
    def energy(self):
        return self._accelerator.energy

    @energy.setter
    def energy(self, value):
        self._accelerator.energy = value

    @property
    def harmonic_number(self):
        return self._accelerator.harmonic_number

    @harmonic_number.setter
    def harmonic_number(self, value):
        return self._accelerator.harmonic_number

    @property
    def cavity_on(self):
        return self._accelerator.cavity_on

    @cavity_on.setter
    def cavity_on(self, value):
        if self._accelerator.harmonic_number < 1:
            raise AcceleratorException('invalid harmonic number')
        self._accelerator.cavity_on = value

    @property
    def radiation_on(self):
        return self._accelerator.radiation_on

    @radiation_on.setter
    def radiation_on(self, value):
        self._accelerator.radiation_on = value

    @property
    def vchamber_on(self):
        return self._accelerator.vchamber_on

    @vchamber_on.setter
    def vchamber_on(self, value):
        self._accelerator.vchamber_on = value
