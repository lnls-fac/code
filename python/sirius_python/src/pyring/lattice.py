import collections
import passmethods
import copy


def findspos(lattice, indices = None):
    if indices is None:
        indices = len(lattice)    
    pos = (len(lattice)+1) * [0.0]
    for i in range(1,len(lattice)+1):
        pos[i] = pos[i-1] + lattice[i-1].length
    pos[-1] = pos[-2] + lattice[-1].length
    if type(indices) is int: 
        return pos[indices]
    else:
        return [pos[i] for i in indices]
    
def findcells(lattice, attribute_name, value = None):
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

def getcellstruct(lattice, attribute_name, indices):
    data = []
    for idx in indices:
        data.append(getattr(lattice[idx], attribute_name))
    return data

def setcellstruct(lattice, attribute_name, indices, values):    
    for idx in range(len(indices)):
        try:
            setattr(lattice[indices[idx]], attribute_name, values[idx])
        except:
            setattr(lattice[indices[idx]], attribute_name, values)
    return lattice

def finddict(lattice, attribute_name):
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
    pass
    #raise Exception('setradiation: not yet implemented')



def flatten(lattice):
    for element in lattice:
        if isinstance(element, collections.Iterable) and not isinstance(element, basestring):
            for line in flatten(element):
                yield line
        else:
            yield element
            
def printlattice(lattice):
    for i in range(len(lattice)):
        print ('Element#  : ' + str(i) + '\n' + str(lattice[i]))
        
def unique(lattice, famname = None):
    idx = findcells(lattice, 'fam_name', famname)
    new_lattice = [element for element in lattice]
    for i in range(len(lattice)):
        if i in idx:
            new_lattice[i] = copy.deepcopy(lattice[i])
    return new_lattice
    
        
        
        