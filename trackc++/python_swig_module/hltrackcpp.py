
import trackcpp as _trackcpp


def _list_str(self):
    return str(list(self))


def _list_repr(self):
    return "'" + _list_str(self) + "'"


_trackcpp.trackcpp_DoubleVector.__repr__ = _list_repr
_trackcpp.trackcpp_DoubleVector.__str__ = _list_str

#class Element(_trackcpp.Element):
#
#    """A lattice element."""
#
#    def __init__(self, fam_name='', length=0.0):
#        super().__init__(fam_name, length)
#
#    @property
#    def poly_a(self):
#        return self.polynom_a
#
#    @poly_a.setter
#    def poly_a(self, value):
#        print(value)
#        #self.polynom_a.clear()
#        #for v in value:
#        #    self.polynom_a.push_back(v)
class Element:

    def __init__(self, fam_name='', length=0.0):
        self._elem = _trackcpp.Element(fam_name, length)

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
        return self._elem.pass_method

    @pass_method.setter
    def pass_method(self, value):
        self._elem.pass_method = value

    @property
    def polynom_a(self):
        return self._elem.polynom_a

    @polynom_a.setter
    def polynom_a(self, value):
        self._elem.polynom_a.clear()
        for v in value:
            self._elem.polynom_a.push_back(v)


class MyClass:
    def __init__(self, x):
        self._x = x

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value * 2
