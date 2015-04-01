
import numpy as _numpy
import trackcpp as _trackcpp
import pyaccel.elements


_ElementVector = _trackcpp.CppElementVector
_TYPE_ERROR_MSG = 'values must be (list) of Element'


class Lattice(object):

    def __init__(self, elements=None, lattice=None):
        if lattice is not None:
            self._lattice = lattice
        elif elements is not None:
            trackcpp_elements = []
            for element in elements:
                trackcpp_elements.append(element._e)
            self._lattice = _ElementVector(trackcpp_elements)
        else:
            self._lattice = _ElementVector()

    def __getitem__(self, index):
        r = self._lattice[index]
        if isinstance(r, _ElementVector):
            out = []
            for e in r:
                out.append(pyaccel.elements.Element(element=e))
        else:
            out = pyaccel.elements.Element(element=r)

        return out

    def __setitem__(self, index, value):
        if isinstance(value, list):
            elements = []
            for v in value:
                if not isinstance(v, pyaccel.elements.Element):
                    raise TypeError(_TYPE_ERROR_MSG)
                elements.append(v._e)
            self._lattice[index] = elements
        elif isinstance(value, pyaccel.elements.Element):
            self._lattice[index] = value._e
        else:
            raise TypeError(_TYPE_ERROR_MSG)

    def __len__(self):
        return len(self._lattice)

    def append(self, value):
        if not isinstance(value, pyaccel.elements.Element):
            raise TypeError(_TYPE_ERROR_MSG)
        self._lattice.append(value._e)


def flatlat(elist):
    """ takes a list-of-list-of-... elements and flattens it: a simple list of lattice elements."""
    flat_elist = []
    for element in elist:
        try:
            famname = element.fam_name
            flat_elist.append(element)
        except:
            flat_elist.extend(flatlat(element))
    return flat_elist


def buildlat(elist):
    """builds lattice from a list of elements and lines"""
    lattice = Lattice()
    elist = flatlat(elist)
    for e in elist:
        lattice.append(e)
    return lattice


def shiftlat(lattice, start):
    new_lattice = lattice[start:]
    for i in range(start):
        new_lattice.append(lattice[i])
    return new_lattice


def findspos(lattice, indices = None):
    """returns longitudinal position of the entrance for all lattice elements"""

    ''' process input '''
    is_number = False
    if indices is None:
        indices = range(len(lattice))
    else:
        try:
            indices[0]
        except:
            is_number = True
            indices = [indices]

    pos = (len(lattice)+1) * [0.0]
    for i in range(1,len(lattice)+1):
        pos[i] = pos[i-1] + lattice[i-1].length
    pos[-1] = pos[-2] + lattice[-1].length
    if is_number:
        return _numpy.array(pos[i])
    else:
        return _numpy.array([pos[i] for i in indices])


def findcells(lattice, attribute_name, value=None):
    """returns a list with indices of elements that match criteria 'attribute_name=value'"""
    indices = []
    for i in range(len(lattice)):
        if hasattr(lattice[i], attribute_name):
            if value == None:
                if getattr(lattice[i], attribute_name) != None:
                    indices.append(i)
            else:
                if getattr(lattice[i], attribute_name) == value:
                    indices.append(i)
    return indices


def getcellstruct(lattice, attribute_name, indices=None):
    """ returns a list with requested lattice data """
    if indices is None:
        indices = range(len(lattice))
    else:
        try:
            indices[0]
        except:
            indices = [indices]

    data = []
    for idx in indices:
        tdata = getattr(lattice[idx], attribute_name)
        data.append(tdata)
    return data


def setcellstruct(lattice, attribute_name, indices, values):
    """ sets elements data and returns a new updated lattice """
    for idx in range(len(indices)):
        if isinstance(values, (tuple, list)):
            setattr(lattice[indices[idx]], attribute_name, values[idx])
        else:
            setattr(lattice[indices[idx]], attribute_name, values)
    return lattice


def finddict(lattice, attribute_name):
    """ returns a dict which correlates values of 'attribute_name' and a list of indices corresponding to matching elements """
    latt_dict = {}
    for i in range(len(lattice)):
        if hasattr(lattice[i], attribute_name):
            att_value = getattr(lattice[i], attribute_name)
            if att_value in latt_dict:
                latt_dict[att_value].append(i)
            else:
                latt_dict[att_value] = [i]
    return latt_dict
