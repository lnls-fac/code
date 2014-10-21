
import ctypes as _ctypes
import trackcpp as _trackcpp


_T_SIZE = 6
_R_SIZE = (6, 6)

_p_translation_vector = _ctypes.c_double*_T_SIZE
_p_rotation_matrix = (_ctypes.c_double*_R_SIZE[1])*_R_SIZE[0]

_t_temp = _p_translation_vector.from_address(0)
_t_class = _t_temp.__class__
del(_t_temp)

_r_temp = _p_rotation_matrix.from_address(0)
_r_class = _r_temp.__class__
del(_r_temp)


class Vector(_t_class):

    def __repr__(self):
        return self._get_str('Vector(', ')')

    def __str__(self):
        return self._get_str()

    def _get_str(self, prefix='', suffix=''):
        vector = []
        for value in self:
            s = "{0: 9.4f}".format(value)
            if len(s) > 9:
                s = "{0: .2e}".format(value)
            vector.append(s)
        return prefix + '[' + ', '.join(vector) + ']' + suffix


class TVector(Vector):
    pass


class RMatrix(list):

    def __repr__(self):
        return self._get_str('RMatrix(', ')')

    def __str__(self):
        return self._get_str()

    def _get_str(self, prefix='', suffix='', commas=False):
        if commas:
            c = ','
        else:
            c = ''
        n = len(prefix)
        rows = [prefix + '[' + self[0].__str__() + c]
        for row in self[1:-1]:
                rows.append(' '*(n+1) + str(row.__str__()) + c)
        rows.append(' '*(n+1) + self[-1].__str__() + ']' + suffix)
        return '\n'.join(rows)


def _get_translation_vector(pointer):
    address = int(pointer)
    array = _p_translation_vector.from_address(address)
    array.__class__ = TVector
    return array


def _get_rotation_matrix(pointer):
    address = int(pointer)
    double_size = _ctypes.sizeof(_ctypes.c_double)
    p = _ctypes.c_double*_R_SIZE[1]
    matrix = RMatrix()
    for i in range(_R_SIZE[0]):
        row = p.from_address(address+i*_R_SIZE[1]*double_size)
        row.__class__ = Vector
        matrix.append(row)
    return matrix


class Element(_trackcpp.Element):
    
    pass_methods = _trackcpp.pm_dict
    _array_names = ['t_in', 't_out']
    _matrix_names = ['r_in', 'r_out']
    _is_initialized = False

    def __init__(self, fam_name, length=0.0):
        super().__init__(fam_name, length)
        self.t_in = _get_translation_vector(self._t_in)
        self.t_out = _get_translation_vector(self._t_out)
        self.r_in = _get_rotation_matrix(self._r_in)
        self.r_out = _get_rotation_matrix(self._r_out)

    def __str__(self):
        s = [''] # get a newline before first attribute
        for name in self.__class__._attributes_to_print:
            if name in Element._array_names:
                value = self.__getattr__(name)[:]
            elif name in Element._matrix_names:
                matrix = self.__getattr__(name)
                num_rows = len(matrix)
                num_cols = len(matrix[0])
                value = str(num_rows) + 'x' + str(num_cols) + ' matrix'
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

    @staticmethod
    def _process_polynoms(polynom_a, polynom_b):
        # makes sure polynom_a and polynom_b have same size and are initialized
        pa, pb = polynom_a, polynom_b
        if pa is None: 
            pa = [0,0,0]
        if pb is None: 
            pb = [0,0,0]
        n = max([3, len(pa), len(pb)])
        for i in range(len(pa),n): pa.append(0.0)
        for i in range(len(pb),n): pb.append(0.0)
        return pa, pb
            

class Marker(Element):

    _attributes_to_print = [
                'fam_name',
                'length',
                'pass_method',
                'hmax',
                'vmax'
        ]
    
    def __init__(self, fam_name):
        """Create a marker element.
        
        Keyword arguments:
        fam_name -- family name
        """
        super().__init__(fam_name, 0.0)
        _trackcpp.initialize_marker(self)


class Bpm(Marker):

    def __init__(self, fam_name):
        """Create a beam position monitor element.

        Keyword arguments:
        fam_name -- family name
        """
        super().__init__(fam_name)


class Drift(Element):

    _attributes_to_print = [
                'fam_name',
                'length',
                'pass_method',
                'hmax',
                'vmax'
        ]
 
    def __init__(self, fam_name, length):
        """Create a drift element.

        Keyword arguments:
        fam_name -- family name
        length -- [m]
        """
        super().__init__(fam_name, length)
        _trackcpp.initialize_drift(self)
       


class Corrector(Element):

    _attributes_to_print = [
                'fam_name',
                'length',
                'pass_method',
                'hmax',
                'vmax',
                'hkick',
                'vkick'
        ]

    def __init__(self, fam_name, hkick, vkick, length = 0.0):
        """Create a corrector element.

        Keyword arguments:
        fam_name -- family name
        length -- [m]
        hkick -- horizontal kick [rad]
        vkick -- vertical kick [rad]
        """
        super().__init__(fam_name, length)
        _trackcpp.initialize_corrector(self, hkick, vkick)
        

class HCorrector(Corrector):

    def __init__(self, fam_name, hkick, length = 0.0):
        """Create a horizontal corrector element.

        Keyword arguments:
        fam_name -- family name
        length -- [m]
        hkick -- horizontal kick [rad]
        """
        super().__init__(fam_name, hkick=hkick, vkick=0.0, length=length)


class VCorrector(Corrector):

    def __init__(self, fam_name, vkick, length = 0.0):
        """Create a vertical corrector element.

        Keyword arguments:
        fam_name -- family name
        length -- [m]
        vkick -- vertical kick [rad]
        """
        super().__init__(fam_name, hkick=0.0, vkick=vkick, length=length)


class Quadrupole(Element):

    _attributes_to_print = [
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
    
    def __init__(self, fam_name, length, K, nr_steps=10):
        """Create a quadrupole element.

        Keyword arguments:
        fam_name -- family name
        length -- [m]
        K -- [m^-2]
        nr_steps -- number of steps (default 1)
        """
        super().__init__(fam_name, length)
        _trackcpp.initialize_quadrupole(self, K, nr_steps)
        


class Sextupole(Element):

    _attributes_to_print = ['fam_name', 'length', 'nr_steps',
                            'polynom_a', 'polynom_b', 'pass_method',
                            'hmax', 'vmax', 'r_in', 'r_out', 't_in', 't_out']
    
    def __init__(self, fam_name, length, S, nr_steps=5):
        """Create a sextupole element.

        Keyword arguments:
        fam_name -- family name
        length -- [m]
        S -- [m^-3]
        nr_steps -- number of steps (default 1)
        """
        super().__init__(fam_name, length)
        _trackcpp.initialize_sextupole(self, S, nr_steps)


class RBend(Element):

    def __init__(self, 
                 fam_name, length, 
                 angle, angle_in=0.0, angle_out=0.0,
                 gap=0.0, fint_in=0.0, fint_out=0.0,
                 polynom_a=None, polynom_b=None,
                 K=None, S=None):
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
        polynom_a, polynom_b = super()._process_polynoms(polynom_a, polynom_b)
        if K is None: K = polynom_b[1]
        if S is None: S = polynom_b[2]
        _trackcpp.initialize_rbend(self, 
                                   angle, angle_in, angle_out, 
                                   gap, fint_in, fint_out,
                                   polynom_a, polynom_b, K, S)


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
#class TVector(_CArray):
#
#    def __repr__(self):
#        return str(self[:])
#
#    def __str__(self):
#        return str(self[:])
#
#
#class RMatrix(_CArray):
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
