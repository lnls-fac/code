
import ctypes as _ctypes
import trackcpp as _trackcpp


_T_SIZE = 6
_R_SIZE = (6, 6)


pass_methods = _trackcpp.pm_dict
array_names = ['t_in', 't_out']
matrix_names = ['r_in', 'r_out']


def _get_double_array(pointer, size):
    address = int(pointer)
    p = _ctypes.c_double*size
    return p.from_address(address)


def _get_double_matrix(pointer, sizes):
    double_size = _ctypes.sizeof(_ctypes.c_double)
    address = int(pointer)
    r = []
    for i in range(sizes[0]):
        p = _ctypes.c_double*sizes[1]
        r.append(p.from_address(address+i*sizes[1]*double_size))
    return r


class Element(_trackcpp.Element):


    def __init__(self, fam_name, length=0.0):
        super().__init__(fam_name, length)
        self.t_in = _get_double_array(self._t_in, _T_SIZE)
        self.t_out = _get_double_array(self._t_out, _T_SIZE)
        self.r_in = _get_double_matrix(self._r_in, _R_SIZE)
        self.r_out = _get_double_matrix(self._r_out, _R_SIZE)

    def __str__(self):
        s = [''] # get a newline before first attribute
        for name in self._attributes_to_print:
            if name in array_names:
                value = self.__getattr__(name)[:]
            else:
                value = self.__getattr__(name)
            formatted_string = _format_string_to_print_element(name, value)
            s.append(formatted_string)
        return '\n'.join(s)

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        else:
            return super().__getattr__(name)


class Marker(Element):

    def __init__(self, fam_name):
        """Create a marker element.
        
        Keyword arguments:
        fam_name -- family name
        """
        super().__init__(fam_name, 0.0)
        _trackcpp.initialize_marker(self)
        self._attributes_to_print = [
                'fam_name',
                'length',
                'pass_method',
                'hmax',
                'vmax'
        ]


class Bpm(Marker):

    def __init__(self, fam_name):
        """Create a beam position monitor element.

        Keyword arguments:
        fam_name -- family name
        """
        super().__init__(fam_name)


class Drift(Element):

    def __init__(self, fam_name, length):
        """Create a drift element.

        Keyword arguments:
        fam_name -- family name
        length -- [m]
        """
        super().__init__(fam_name, length)
        _trackcpp.initialize_drift(self)
        self._attributes_to_print = [
                'fam_name',
                'length',
                'pass_method',
                'hmax',
                'vmax'
        ]


class Corrector(Element):

    def __init__(self, fam_name, length, hkick, vkick):
        """Create a corrector element.

        Keyword arguments:
        fam_name -- family name
        length -- [m]
        hkick -- horizontal kick [rad]
        vkick -- vertical kick [rad]
        """
        super().__init__(fam_name, length)
        _trackcpp.initialize_corrector(self, hkick, vkick)
        self._attributes_to_print = [
                'fam_name',
                'length',
                'pass_method',
                'hmax',
                'vmax',
                'hkick',
                'vkick'
        ]


class HCorrector(Corrector):

    def __init__(self, fam_name, length, hkick):
        """Create a horizontal corrector element.

        Keyword arguments:
        fam_name -- family name
        length -- [m]
        hkick -- horizontal kick [rad]
        """
        super().__init__(fam_name, length, hkick=hkick, vkick=0.0)


class VCorrector(Corrector):

    def __init__(self, fam_name, length, vkick):
        """Create a vertical corrector element.

        Keyword arguments:
        fam_name -- family name
        length -- [m]
        vkick -- vertical kick [rad]
        """
        super().__init__(fam_name, length, hkick=0.0, vkick=vkick)


class Quadrupole(Element):

    def __init__(self, fam_name, length, K, nr_steps=1):
        """Create a quadrupole element.

        Keyword arguments:
        fam_name -- family name
        length -- [m]
        K -- [m^-2]
        nr_steps -- number of steps (default 1)
        """
        super().__init__(fam_name, length)
        _trackcpp.initialize_quadrupole(self, K, nr_steps)
        self._attributes_to_print = [
                'fam_name',
                'length',
                'nr_steps',
                'polynom_a',
                'polynom_b',
                'pass_method',
                'hmax',
                'vmax',
                'r_in',
                'r_out',
                't_in',
                't_out'
        ]


class Sextupole(Element):

    def __init__(self, fam_name, length, S, nr_steps=1):
        """Create a sextupole element.

        Keyword arguments:
        fam_name -- family name
        length -- [m]
        S -- [m^-3]
        nr_steps -- number of steps (default 1)
        """
        super().__init__(fam_name, length)
        _trackcpp.initialize_sextupole(self, S, nr_steps)
        self._attributes_to_print = [
                'fam_name',
                'length',
                'nr_steps',
                'polynom_a',
                'polynom_b',
                'pass_method',
                'hmax',
                'vmax',
                'r_in',
                'r_out',
                't_in',
                't_out'
        ]


class RBend(Element):

    def __init__(self, fam_name, length, angle, angle_in=0.0, angle_out=0.0,
            K=0.0, S=0.0):
        """Create a rectangular dipole element.

        Keyword arguments:
        fam_name -- family name
        length -- [m]
        angle -- [rad]
        angle_in -- [rad]
        angle_out -- [rad]
        K -- [m^-2]
        S -- [m^-3]
        """
        super().__init__(fam_name, length)
        _trackcpp.initialize_rbend(self, angle, angle_in, angle_out, K, S)


class RFCavity(Element):

    def __init__(self, fam_name, length, frequency, voltage):
        """Create an RF cavity element.

        Keyword arguments:
        fam_name -- family name
        length -- [m]
        frequency -- [Hz]
        voltage -- [V]
        """
        super().__init__(fam_name, length)
        _trackcpp.initialize_rfcavity(self, frequency, voltage)


def _list_repr(self):
    return str(list(self))


def _list_str(self):
    return str(list(self))


def _format_string_to_print_element(name, value):
    s = "{0:>15}: {1}".format(name, str(value))
    return s


_trackcpp.CppDoubleVector.__repr__ = _list_repr
_trackcpp.CppDoubleVector.__str__ = _list_str


#class PassMethodError(Exception):
#    pass
#
#
#class LengthError(Exception):
#    pass
#
#
#class _CArray:
#
#    def __init__(self, array, size):
#        self._array = array
#        self._size = size
#
#    def __getitem__(self, k):
#        idx = self._check_and_get_indices(k, self._size)
#        if idx is None:
#            r = _trackcpp.c_array_get(self._array, k%self._size)
#        else:
#            r = []
#            for i in idx:
#                r.append(_trackcpp.c_array_get(self._array, i))
#        return r
#
#    def __setitem__(self, k, value):
#        idx = self._check_and_get_indices(k, self._size)
#        if idx is None:
#            if not isinstance(value, int):
#                raise TypeError('value must be int')
#            _trackcpp.c_array_set(self._array, k%self._size, value)
#        else:
#            n = len(value)
#            if not n == len(idx):
#                raise LengthError('lengths must be equal')
#            for t in zip(idx, range(n)):
#                _trackcpp.c_array_set(self._array, t[0], value[t[1]])
#
#    def _check_and_get_indices(self, k, size):
#        if isinstance(k, int):
#            if not -size <= k < size:
#                raise IndexError('index out of range')
#            idx = None
#        elif isinstance(k, slice):
#            k_indices = k.indices(size)
#            idx = range(*k_indices)
#        elif isinstance(k, list) or isinstance(k, tuple):
#            if not 0 <= min(k) and size <= max(k):
#                raise IndexError('index out of range')
#            idx = k
#        else:
#            raise TypeError('indices must be numbers, not ' + type(k))
#
#        return idx
#
#
#class TranslationVector(_CArray):
#
#    def __repr__(self):
#        return str(self[:])
#
#    def __str__(self):
#        return str(self[:])
#
#
#class RotationMatrix(_CArray):
#
#    def __init__(self, array, size):
#        if not isinstance(size, tuple):
#            raise TypeError('size must be tuple')
#        if not len(size) == 2:
#            raise LengthError('matrix must have two sizes')
#
#        self._rows = size[0]
#        self._cols = size[1]
#        self._m_size = (self._rows, self._cols)
#        super().__init__(array, self._rows*self._cols)
#
#    def __getitem__(self, k):
#        self._check_matrix_indices(k)
#        if isinstance(k[0], int) and isinstance(k[1], int):
#            m_idx = self._rows*k[0] + k[1]
#            return _trackcpp.c_array_get(self._array, m_idx)
#        else:
#            idx = []
#            for z in zip(k, self._m_size):
#                i_temp = self._check_and_get_indices(z[0], z[1])
#                if i_temp is None:
#                    idx.append([z[0]])
#                else:
#                    idx.append(i_temp)
#            m = []
#            for i in idx[0]:
#                m.append([])
#                for j in idx[1]:
#                    m_idx = self._rows*i + j
#                    m[-1].append(_trackcpp.c_array_get(self._array, m_idx))
#            return m
#
#    def __setitem__(self, k, value):
#        self._check_matrix_indices(k)
#        if isinstance(k[0], int) and isinstance(k[1], int):
#            if not isinstance(value, (int, float)):
#                raise TypeError('value must be number')
#            if (not -self._rows <= k[0] < self._rows and
#                    not -self._cols <= k[1] < self._cols):
#                raise IndexError('index out of range')
#            m_idx = self._rows*(k[0]%self._rows) + (k[1]%self._cols)
#            _trackcpp.c_array_set(self._array, m_idx, value)
#        else:
#            if not isinstance(value, (list, tuple)):
#                raise TypeError('value must be matrix')
#            for row in value:
#                if not isinstance(row, (list, tuple)):
#                    raise TypeError('value must be matrix')
#            idx = []
#            for z in zip(k, self._m_size):
#                i_temp = self._check_and_get_indices(z[0], z[1])
#                if i_temp is None:
#                    idx.append([z[0]%z[1]])
#                else:
#                    idx.append(i_temp)
#            if not len(idx[0]) == len(value):
#                raise LengthError('wrong number of rows')
#            if not len(idx[1]) == len(value[0]):
#                raise LengthError('wrong number of columns')
#            for z in zip(idx[0], range(len(value))):
#                for w in zip(idx[1], range(len(value[0]))):
#                    m_idx = self._rows*z[0] + w[0]
#                    x = value[z[1]][w[1]]
#                    _trackcpp.c_array_set(self._array, m_idx, x)
#
#    def _check_matrix_indices(self, k):
#        if not isinstance(k, tuple):
#            raise TypeError('indices must be tuple')
#        if not len(k) == 2:
#            raise LengthError('two indices are needed')
