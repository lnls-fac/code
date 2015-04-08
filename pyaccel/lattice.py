
import numpy as _numpy
import trackcpp as _trackcpp
import pyaccel.accelerator
import pyaccel.elements

def flatlat(elist):
    """ takes a list-of-list-of-... elements and flattens it: a simple list of lattice elements """
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
    lattice = _trackcpp.CppElementVector()
    elist = flatlat(elist)
    for e in elist:
        lattice.append(e._e)
    return lattice


def shiftlat(lattice, start):
    """ shift periodically the lattic so that it starts at element whose index is 'start' """
    new_lattice = lattice[start:]
    for i in range(start):
        new_lattice.append(lattice[i])
    return new_lattice


def lengthlat(lattice):
    len = [e.length for e in lattice]
    return sum(len)

def findspos(lattice, indices = None):
    """ returns longitudinal position of the entrance for all lattice elements """

    is_number = False
    if indices is None:
        indices = range(len(lattice))
    else:
        try:
            indices[0]
        except:
            is_number = True

    pos = (len(lattice)+1) * [0.0]
    for i in range(1,len(lattice)+1):
        pos[i] = pos[i-1] + lattice[i-1].length
    pos[-1] = pos[-2] + lattice[-1].length
    if is_number:
        return pos[indices]
    else:
        return _numpy.array([pos[i] for i in indices])

def findcells(lattice, attribute_name, value=None):
    """ returns a list with indices of elements that match criteria 'attribute_name=value' """
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

def getcellstruct(lattice, attribute_name, indices = None, m=None, n=None):
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
        if n is None:
            if m is None:
                data.append(tdata)
            else:
                data.append(tdata[m])
        else:
            if m is None:
                data.append(tdata)
            else:
                data.append(tdata[m][n])
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


def get_rf_frequency(lattice):
    """ Returns the frequency of the first RF cavity in the lattice """
    for e in lattice:
        if e.frequency != 0:
            return e.frequency
