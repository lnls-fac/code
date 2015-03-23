
import ctypes as _ctypes
import numpy as _numpy
import trackcpp as _trackcpp


_NUM_COORDS = 6
_DIMS = (_NUM_COORDS, _NUM_COORDS)
_coord_vector = _ctypes.c_double*_NUM_COORDS
_coord_matrix = _ctypes.c_double*_DIMS[0]*_DIMS[1]

pass_methods = _trackcpp.pm_dict


class Element(object):

    t_valid_types = (list, _numpy.ndarray)
    r_valid_types = (_numpy.ndarray)

    def __init__(self, fam_name="", length=0.0, element=None):
        if element is None:
            self._e = _trackcpp.Element(fam_name, length)
        else:
            self._e = element

    @property
    def fam_name(self):
        return self._e.fam_name

    @fam_name.setter
    def fam_name(self, value):
        self._e.fam_name = value

    @property
    def pass_method(self):
        return pass_methods[self._e.pass_method]

    @pass_method.setter
    def pass_method(self, value):
        if isinstance(value, str):
            if value not in pass_methods:
                raise ValueError("pass method '" + value + "' not found")
            else:
                self._e.pass_method = pass_methods.index(value)
        elif isinstance(self, int):
            if not (0 <= value < len(pass_methods)):
                raise IndexError("pass method index out of range")
            else:
                self._e.pass_method = value
        else:
            raise TypeError("pass method value must be string or index")

    @property
    def length(self):
        return self._e.length

    @length.setter
    def length(self, value):
        self._e.length = value

    @property
    def num_steps(self):
        return self._e.nr_steps

    @num_steps.setter
    def num_steps(self, value):
        self._e.nr_steps = value

    @property
    def hkick(self):
        return self._e.hkick

    @hkick.setter
    def hkick(self, value):
        self._e.hkick = value

    @property
    def vkick(self):
        return self._e.vkick

    @vkick.setter
    def vkick(self, value):
        self._e.vkick = value

    @property
    def angle(self):
        return self._e.angle

    @angle.setter
    def angle(self, value):
        self._e.angle = value

    @property
    def angle_in(self):
        return self._e.angle_in

    @angle_in.setter
    def angle_in(self, value):
        self._e.angle_in = value

    @property
    def angle_out(self):
        return self._e.angle_out

    @angle_out.setter
    def angle_out(self, value):
        self._e.angle_out = value

    @property
    def gap(self):
        return self._e.gap

    @gap.setter
    def gap(self, value):
        self._e.gap = value

    @property
    def fint_in(self):
        return self._e.fint_in

    @fint_in.setter
    def fint_in(self, value):
        self._e.fint_in = value

    @property
    def fint_out(self):
        return self._e.fint_out

    @fint_out.setter
    def fint_out(self, value):
        self._e.fint_out = value

    @property
    def thin_KL(self):
        return self._e.thin_KL

    @thin_KL.setter
    def thin_KL(self, value):
        self._e._thin_KL = value

    @property
    def thin_SL(self):
        return self._e.thin_SL

    @thin_SL.setter
    def thin_SL(self, value):
        self._e._thin_SL = value

    @property
    def frequency(self):
        return self._e.frequency

    @frequency.setter
    def frequency(self, value):
        self._e.frequency = value

    @property
    def voltage(self):
        return self._e.voltage

    @voltage.setter
    def voltage(self, value):
        self._e.voltage = value

    @property
    def polynom_a(self):
        return _numpy.array(self._e.polynom_a)

    @polynom_a.setter
    def polynom_a(self, value):
        self._check_type_is_list_like(value)
        self._e.polynom_a.clear()
        for x in value:
            self._e.polynom_a.append(x)

    @property
    def polynom_b(self):
        return _numpy.array(self._e.polynom_b)

    @polynom_b.setter
    def polynom_b(self, value):
        self._check_type_is_list_like(value)
        self._e.polynom_b.clear()
        for x in value:
            self._e.polynom_b.append(x)

    '''IMPLEMENT'''
    # const Kicktable* kicktable;

    @property
    def hmax(self):
        return self._e.hmax

    @hmax.setter
    def hmax(self, value):
        self._e.hmax = value

    @property
    def vmax(self):
        return self._e.vmax

    @vmax.setter
    def vmax(self, value):
        self._e.vmax = value

    @property
    def t_in(self):
        return self._get_coord_vector(self._e.t_in)
        # return self._get_vector_from_c_array(self._e.t_in, _NUM_COORDS)

    @t_in.setter
    def t_in(self, value):
        self._check_type(value, Element.t_valid_types)
        self._check_size(value, _NUM_COORDS)
        self._set_c_array_from_vector(self._e.t_in, _NUM_COORDS, value)

    @property
    def t_out(self):
        return self._get_coord_vector(self._e.t_out)
        # return self._get_vector_from_c_array(self._e.t_out, _NUM_COORDS)

    @t_out.setter
    def t_out(self, value):
        self._check_type(value, Element.t_valid_types)
        self._check_size(value, _NUM_COORDS)
        self._set_c_array_from_vector(self.e._t_out, _NUM_COORDS, value)

    @property
    def r_in(self):
        return self._get_coord_matrix(self._e.r_in)
        # return self._get_matrix_from_c_array(self._e.r_in, _DIMS)

    @r_in.setter
    def r_in(self, value):
        self._check_type(value, Element.r_valid_types)
        self._check_size(value, _DIMS)
        self._set_c_array_from_matrix(self._e.r_in, _DIMS, value)

    @property
    def r_out(self):
        return self._get_coord_matrix(self._e.r_out)
        # return self._get_matrix_from_c_array(self._e.r_out, _DIMS)

    @r_out.setter
    def r_out(self, value):
        self._check_type(value, Element.r_valid_types)
        self._check_size(value, _DIMS)
        self._set_c_array_from_matrix(self._e.r_out, _DIMS, value)

    # def _get_vector_from_c_array(self, array, size):
    #     r = []
    #     for i in range(size):
    #         r.append(_trackcpp.c_array_get(array, i))
    #
    #     return _numpy.array(r)

    def _set_c_array_from_vector(self, array, size, values):
        if not (size == len(values)):
            raise ValueError("array and vector must have same size")
        for i in range(size):
            _trackcpp.c_array_set(array, i, values[i])

    # def _get_matrix_from_c_array(self, array, shape):
    #     rows, cols = shape
    #     r = []
    #     for i in range(rows):
    #         r.append([])
    #         for j in range(cols):
    #             r[-1].append(_trackcpp.c_array_get(array, i*cols + j))
    #
    #     return _numpy.array(r)

    def _set_c_array_from_matrix(self, array, shape, values):
        if not (shape == values.shape):
            raise ValueError("array and matrix must have same shape")
        rows, cols = shape
        for i in range(rows):
            for j in range(cols):
                _trackcpp.c_array_set(array, i*cols + j, values[i, j])

    def _check_type(self, value, types):
        r = False
        for t in types:
            r = r or isinstance(value, t)
        if not r:
            raise TypeError("value must be list or numpy.ndarray")

    def _check_size(self, value, size):
        if not len(value) == size:
            raise ValueError("size must be " + str(size))

    def _get_coord_vector(self, pointer):
        address = int(pointer)
        c_array = _coord_vector.from_address(address)
        return _numpy.ctypeslib.as_array(c_array)

    def _get_coord_matrix(self, pointer):
        address = int(pointer)
        c_array = _coord_matrix.from_address(address)
        return _numpy.ctypeslib.as_array(c_array)
