
import trackcpp as _trackcpp


_T_SIZE = 6
_R_SIZE = (6, 6)


def _list_repr(self):
    return str(list(self))


def _list_str(self):
    return str(list(self))


_trackcpp.cppDoubleVector.__repr__ = _list_repr
_trackcpp.cppDoubleVector.__str__ = _list_str


pass_methods = _trackcpp.pm_dict


class PassMethodError(Exception):
    pass


class LengthError(Exception):
    pass


class Element:

    "A lattice element."

    def __init__(self, element=None):
        if element is not None:
            self._elem = element
        else:
            self._elem = _trackcpp.Element('', 0.0)
        self._t_in = TranslationVector(self._elem.t_in, _T_SIZE)
        self._t_out = TranslationVector(self._elem.t_out, _T_SIZE)
        self._r_in = RotationMatrix(self._elem.r_in, _R_SIZE)
        self._r_out = RotationMatrix(self._elem.r_out, _R_SIZE)

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

    @property
    def t_out(self):
        return self._t_out

    @t_out.setter
    def t_out(self, value):
        if isinstance(value, TranslationVector):
            self._t_out = value
        else:
            self._t_out[:] = value

    @property
    def r_in(self):
        return self._r_in


class _CArray:

    def __init__(self, array, size):
        self._array = array
        self._size = size

    def __getitem__(self, k):
        idx = self._check_and_get_indices(k, self._size)
        if idx is None:
            r = _trackcpp.c_array_get(self._array, k%self._size)
        else:
            r = []
            for i in idx:
                r.append(_trackcpp.c_array_get(self._array, i))
        return r

    def __setitem__(self, k, value):
        idx = self._check_and_get_indices(k, self._size)
        if idx is None:
            if not isinstance(value, int):
                raise TypeError('value must be int')
            _trackcpp.c_array_set(self._array, k%self._size, value)
        else:
            n = len(value)
            if not n == len(idx):
                raise LengthError('lengths must be equal')
            for t in zip(idx, range(n)):
                _trackcpp.c_array_set(self._array, t[0], value[t[1]])

    def _check_and_get_indices(self, k, size):
        if isinstance(k, int):
            if not -size <= k < size:
                raise IndexError('index out of range')
            idx = None
        elif isinstance(k, slice):
            k_indices = k.indices(size)
            idx = range(*k_indices)
        elif isinstance(k, list) or isinstance(k, tuple):
            if not 0 <= min(k) and size <= max(k):
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


class RotationMatrix(_CArray):

    def __init__(self, array, size):
        if not isinstance(size, tuple):
            raise TypeError('size must be tuple')
        if not len(size) == 2:
            raise LengthError('matrix must have two sizes')

        self._rows = size[0]
        self._cols = size[1]
        self._m_size = (self._rows, self._cols)
        super().__init__(array, self._rows*self._cols)

    def __getitem__(self, k):
        self._check_matrix_indices(k)
        if isinstance(k[0], int) and isinstance(k[1], int):
            m_idx = self._rows*k[0] + k[1]
            return _trackcpp.c_array_get(self._array, m_idx)
        else:
            idx = []
            for z in zip(k, self._m_size):
                i_temp = self._check_and_get_indices(z[0], z[1])
                if i_temp is None:
                    idx.append([z[0]])
                else:
                    idx.append(i_temp)
            m = []
            for i in idx[0]:
                m.append([])
                for j in idx[1]:
                    m_idx = self._rows*i + j
                    m[-1].append(_trackcpp.c_array_get(self._array, m_idx))
            return m

    def __setitem__(self, k, value):
        self._check_matrix_indices(k)
        if isinstance(k[0], int) and isinstance(k[1], int):
            if not isinstance(value, (int, float)):
                raise TypeError('value must be number')
            if (not -self._rows <= k[0] < self._rows and
                    not -self._cols <= k[1] < self._cols):
                raise IndexError('index out of range')
            m_idx = self._rows*(k[0]%self._rows) + (k[1]%self._cols)
            _trackcpp.c_array_set(self._array, m_idx, value)
        else:
            if not isinstance(value, (list, tuple)):
                raise TypeError('value must be matrix')
            for row in value:
                if not isinstance(row, (list, tuple)):
                    raise TypeError('value must be matrix')
            idx = []
            for z in zip(k, self._m_size):
                i_temp = self._check_and_get_indices(z[0], z[1])
                if i_temp is None:
                    idx.append([z[0]%z[1]])
                else:
                    idx.append(i_temp)
            if not len(idx[0]) == len(value):
                raise LengthError('wrong number of rows')
            if not len(idx[1]) == len(value[0]):
                raise LengthError('wrong number of columns')
            for z in zip(idx[0], range(len(value))):
                for w in zip(idx[1], range(len(value[0]))):
                    m_idx = self._rows*z[0] + w[0]
                    x = value[z[1]][w[1]]
                    _trackcpp.c_array_set(self._array, m_idx, x)

    def _check_matrix_indices(self, k):
        if not isinstance(k, tuple):
            raise TypeError('indices must be tuple')
        if not len(k) == 2:
            raise LengthError('two indices are needed')


class Marker(Element):
    
    def __init__(self, fam_name):
        e = _trackcpp.Element_marker(fam_name)
        super().__init__(e)


class Bpm(Element):

    def __init__(self, fam_name):
        e = _trackcpp.Element_bpm(fam_name)
        super().__init__(e)


class Drift(Element):

    def __init__(self, fam_name, length):
        e = _trackcpp.Element_drift(fam_name, length)
        super().__init__(e)


class Corrector(Element):

    def __init__(self, fam_name, length, hkick, vkick):
        e = _trackcpp.Element_corrector(fam_name, length, hkick, vkick)
        super().__init__(e)


class HCorrector(Corrector):

    def __init__(self, fam_name, length, hkick):
        super().__init__(fam_name, length, hkick, 0.0)


class VCorrector(Corrector):

    def __init__(self, fam_name, length, vkick):
        super().__init__(fam_name, length, 0.0, vkick)


class Quadrupole(Element):

    def __init__(self, fam_name, length, K, nr_steps=1):
        e = _trackcpp.Element_quadrupole(fam_name, length, K, nr_steps)
        super().__init__(e)


class Sextupole(Element):

    def __init__(self, fam_name, length, S, nr_steps=1):
        e = _trackcpp.Element_sextupole(fam_name, length, S, nr_steps)
        super().__init__(e)


class RBend(Element):

    def __init__(self, fam_name, length, angle, angle_in=0.0, angle_out=0.0,
                 K=0.0, S=0.0):
        e = _trackcpp.Element_rbend(fam_name, length, angle,
                                    angle_in, angle_out, K, S)
        super().__init__(e)


class RFCavity(Element):

    def __init__(self, fam_name, length, frequency, voltage):
        e = _trackcpp.Element_rfcavity(fam_name, length, frequency, voltage)
        super().__init__(e)
