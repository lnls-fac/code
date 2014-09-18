import collections
import passmethods
import copy


def findspos(lattice, indices = None):
    """ returns longitudinal position of the entrance for all lattice elements """
    
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
        return pos[i]
    else:
        return [pos[i] for i in indices]
    
def findcells(lattice, attribute_name, value = None):
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

def getcellstruct(lattice, attribute_name, indices = None):
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
        try:
            setattr(lattice[indices[idx]], attribute_name, values[idx])
        except:
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


def setcavity(lattice, state):
    """ sets state of cavities: on or off """
    state = state.upper()
    if state == 'ON':
        pass_method = passmethods.cavity_pass
    elif state == 'OFF':
        pass_method = passmethods.identity_pass
    else:
        raise Exception('cavity state not defined!')
    indices = findcells(lattice, 'frequency')
    for idx in indices:
        lattice[idx].pass_method = pass_method
    return lattice
        
def setradiation(lattice, state):
    """ turns ratiative effects on or off """
    return lattice
    #raise Exception('setradiation: not yet implemented')



def flatten(lattice):
    """ takes a list-of-list-of-... elements and flattens it: a simple list of lattice elements."""
    for element in lattice:
        if isinstance(element, collections.Iterable) and not isinstance(element, basestring):
            for line in flatten(element):
                yield line
        else:
            yield element
            
def printlattice(lattice):
    """ prints elements info of a lattice """
    for i in range(len(lattice)):
        print ('Element#  : ' + str(i) + '\n' + str(lattice[i]))
        
def unique(lattice, famname = None):
    idx = findcells(lattice, 'fam_name', famname)
    new_lattice = [element for element in lattice]
    for i in range(len(lattice)):
        if i in idx:
            new_lattice[i] = copy.deepcopy(lattice[i])
    return new_lattice
    
        
        
        