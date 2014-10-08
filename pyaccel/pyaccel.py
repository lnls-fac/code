
import trackcpp.trackcpp as _trackcpp


_T_SIZE = 6
_R_SIZE = (6, 6)


def _list_repr(self):
    return str(list(self))


def _list_str(self):
    return str(list(self))


_trackcpp.trackcpp_DoubleVector.__repr__ = _list_repr
_trackcpp.trackcpp_DoubleVector.__str__ = _list_str


pass_methods = _trackcpp.pm_dict


class PassMethodError(Exception):
    pass


class LengthError(Exception):
    pass


class Element:

    "A lattice element."

    def __init__(self, fam_name='', length=0.0):
        self._elem = _trackcpp.Element(fam_name, length)
        self._t_in = TranslationVector(self._elem.t_in, _T_SIZE)

    @property
    def fam_name(self):
        return self._elem.fam_name

    @fam_name.setter
    def fam_name(self, value):
        self._elem.fam_name = value

    @property
    def length(self):
        return self._elem.length

    @length.setter
    def length(self, value):
        self._elem.length = value

    @property
    def pass_method(self):
        return _trackcpp.pm_dict[self._elem.pass_method]

    @pass_method.setter
    def pass_method(self, value):
        try:
            idx = _trackcpp.pm_dict.index(value)
            self._elem.pass_method = idx
        except:
            raise PassMethodError('pass method not found')

    @property
    def nr_steps(self):
        return self._elem.nr_steps

    @nr_steps.setter
    def nr_steps(self, value):
        self._elem.nr_steps = value
    
    @property
    def hkick(self):
        return self._elem.hkick

    @hkick.setter
    def hkick(self, value):
        self._elem.hkick = value

    @property
    def vkick(self):
        return self._elem.vkick

    @vkick.setter
    def vkick(self, value):
        self._elem.vkick = value

    @property
    def angle(self):
        return self._elem.angle

    @angle.setter
    def angle(self, value):
        self._elem.angle = value

    @property
    def angle_in(self):
        return self._elem.angle_in

    @angle_in.setter
    def angle_in(self, value):
        self._elem.angle_in = value

    @property
    def angle_out(self):
        return self._elem.angle_out

    @angle_out.setter
    def angle_out(self, value):
        self._elem.angle_out = value

    @property
    def gap(self):
        return self._elem.gap

    @gap.setter
    def gap(self, value):
        self._elem.gap = value

    @property
    def fint_in(self):
        return self._elem.fint_in

    @fint_in.setter
    def fint_in(self, value):
        self._elem.fint_in = value

    @property
    def fint_out(self):
        return self._elem.fint_out

    @fint_out.setter
    def fint_out(self, value):
        self._elem.fint_out = value

    @property
    def thin_KL(self):
        return self._elem.thin_KL

    @thin_KL.setter
    def thin_KL(self, value):
        self._elem.thin_KL = value
    
    @property
    def thin_SL(self):
        return self._elem.thin_SL

    @thin_SL.setter
    def thin_SL(self, value):
        self._elem.thin_SL = value

    @property
    def frequency(self):
        return self._elem.frequency

    @frequency.setter
    def frequency(self, value):
        self._elem.frequency = value
    
    @property
    def voltage(self):
        return self._elem.voltage

    @voltage.setter
    def voltage(self, value):
        self._elem.voltage = value
    
    @property
    def polynom_a(self):
        return self._elem.polynom_a

    @polynom_a.setter
    def polynom_a(self, value):
        self._elem.polynom_a.clear()
        for v in value:
            self._elem.polynom_a.push_back(v)
    
    @property
    def polynom_b(self):
        return self._elem.polynom_b

    @polynom_b.setter
    def polynom_b(self, value):
        self._elem.polynom_b.clear()
        for v in value:
            self._elem.polynom_b.push_back(v)

    @property
    def kicktable(self):
        return self._elem.kicktable

    @kicktable.setter
    def kicktable(self, value):
        self._elem.kicktable = value

    @property
    def hmax(self):
        return self._elem.hmax

    @hmax.setter
    def hmax(self, value):
        self._elem.hmax = value

    @property
    def vmax(self):
        return self._elem.vmax

    @vmax.setter
    def vmax(self, value):
        self._elem.vmax = value

    @property
    def t_in(self):
        return self._t_in

    @t_in.setter
    def t_in(self, value):
        if isinstance(value, TranslationVector):
            self._t_in = value
        else:
            self._t_in[:] = value


class _CArray:

    def __init__(self, array, size):
        self._array = array
        self._size = size

    def __getitem__(self, k):
        idx = self._get_and_check_indices(k)
        if idx is None:
            r = _trackcpp.c_array_get(self._array, k%self._size)
        else:
            r = []
            for i in idx:
                r.append(_trackcpp.c_array_get(self._array, i))
        return r

    def __setitem__(self, k, value):
        idx = self._get_and_check_indices(k)
        if idx is None:
            _trackcpp.c_array_set(self._array, k%self._size, value)
        else:
            n = len(value)
            if not n == len(idx):
                raise LengthError('lengths must be equal')
            for t in zip(idx, range(n)):
                _trackcpp.c_array_set(self._array, t[0], value[t[1]])

    def _get_and_check_indices(self, k):
        if isinstance(k, int):
            if not -self._size <= k < self._size:
                raise IndexError('index out of range')
            idx = None
        elif isinstance(k, slice):
            start, stop, step = k.indices(self._size)
            idx = range(start, stop, step)
        elif isinstance(k, list) or isinstance(k, tuple):
            if not 0 <= min(k) and self._size <= max(k):
                raise IndexError('index out of range')
            idx = k
        else:
            raise TypeError('indices must be numbers, not ' + type(k))

        return idx


class TranslationVector(_CArray):

    def __repr__(self):
        return str(self[:])

    def __str__(self):
        return str(self[:])
