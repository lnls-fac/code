
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

pass_methods = _trackcpp.pm_dict


class Vector(_t_class):

    #def __repr__(self):
    #    return self._get_str('Vector(', ')')

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

    #def __repr__(self):
    #    return self._get_str('RMatrix(', ')')

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

    _attributes_to_print = [
            'fam_name',
            'length',
            'pass_method',
            'hmax',
            'vmax'
    ]
    
    _array_names = ['t_in', 't_out']
    _matrix_names = ['r_in', 'r_out']

    def __init__(self, fam_name, length=0.0):
        super().__init__(fam_name, length)
        self.t_in = _get_translation_vector(self._t_in)
        self.t_out = _get_translation_vector(self._t_out)
        self.r_in = _get_rotation_matrix(self._r_in)
        self.r_out = _get_rotation_matrix(self._r_out)

    #def __repr__(self):
    #    return self.__str__()

    def __str__(self):
        s = [] # get a newline before first attribute
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

    def _get_pass_method(self):
        return pass_methods[self._pass_method]

    def _set_pass_method(self, value):
        print('oi')
        if isinstance(value, int):
            if (0 <= value < len(pass_methods)):
                self._pass_method = value
            else:
                raise ValueError('pass method out of range')
        elif isinstance(value, str):
            try:
                index = pass_methods.index(value)
            except:
                raise ValueError('pass method not found')
        else:
            raise TypeError('pass method must be int or str')

    pass_method = property(_get_pass_method, _set_pass_method)
            

class Marker(Element):

    _attributes_to_print = ['fam_name', 'pass_method', 'hmax', 'vmax']
    
    def __init__(self, fam_name):
        """Create a marker element.
        
        Keyword arguments:
        fam_name -- family name
        """
        super().__init__(fam_name, 0.0)
        _trackcpp.initialize_marker(self)


class Bpm(Marker):

    _attributes_to_print = ['fam_name', 'pass_method', 'length', 'hmax', 'vmax']
    
    def __init__(self, fam_name):
        """Create a beam position monitor element.

        Keyword arguments:
        fam_name -- family name
        """
        super().__init__(fam_name)


class Drift(Element):

    _attributes_to_print = ['fam_name', 'pass_method', 'length', 'hmax', 'vmax']
 
    def __init__(self, fam_name, length):
        """Create a drift element.

        Keyword arguments:
        fam_name -- family name
        length -- [m]
        """
        super().__init__(fam_name, length)
        _trackcpp.initialize_drift(self)
       


class Corrector(Element):

    _attributes_to_print = ['fam_name', 'pass_method', 'length', 'hkick', 'vkick', 'hmax', 'vmax']

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

    _attributes_to_print = ['fam_name', 'pass_method', 'length', 'hkick', 'hmax', 'vmax']
    
    def __init__(self, fam_name, hkick, length = 0.0):
        """Create a horizontal corrector element.

        Keyword arguments:
        fam_name -- family name
        length -- [m]
        hkick -- horizontal kick [rad]
        """
        super().__init__(fam_name, hkick=hkick, vkick=0.0, length=length)


class VCorrector(Corrector):

    _attributes_to_print = ['fam_name', 'pass_method', 'length', 'vkick', 'hmax', 'vmax']
    
    def __init__(self, fam_name, vkick, length = 0.0):
        """Create a vertical corrector element.

        Keyword arguments:
        fam_name -- family name
        length -- [m]
        vkick -- vertical kick [rad]
        """
        super().__init__(fam_name, hkick=0.0, vkick=vkick, length=length)


class Quadrupole(Element):

    _attributes_to_print = ['fam_name', 'pass_method', 'length', 'nr_steps',
                            'polynom_a', 'polynom_b', 'hmax', 'vmax', 
                            'r_in', 'r_out', 't_in', 't_out']
    
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

    _attributes_to_print = ['fam_name', 'pass_method', 'length', 'nr_steps',
                            'polynom_a', 'polynom_b', 'hmax', 'vmax', 
                            'r_in', 'r_out', 't_in', 't_out']
    
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

    _attributes_to_print = ['fam_name', 'pass_method', 'length', 'nr_steps',
                            'angle', 'angle_in', 'angle_out',
                            'gap', 'fint_in', 'fint_out',
                            'polynom_a', 'polynom_b', 'hmax', 'vmax', 
                            'r_in', 'r_out', 't_in', 't_out']
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

    _attributes_to_print = ['fam_name', 'pass_method', 'length', 
                            'frequency', 'voltage', 'hmax', 'vmax']
    
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
