import passmethods
import trackcpp

servers = {
    'pyring'   : 0,
    'trackcpp' : 1,
    'trackmgr' : 2,
}

default_server = servers['pyring']

class Tracking:

    @staticmethod
    def track1turn_pyring(lattice, pos):
        for element in lattice:
            #print(element)
            (_, pm_map) = passmethods.pm_dict[element.pass_method]
            pm_map(pos, element)
        return pos

    @staticmethod
    def track1turn_trackcpp(lattice, pos):
        return trackcpp.track1turn(lattice, pos)
        if type(pos) is list:
            return trackcpp.track1turn(lattice, pos)
        else:
            raise Exception('Error in pos type')


def track1turn(lattice, pos):
    if default_server == servers['pyring']:
        return Tracking.track1turn_pyring(lattice, pos)
    elif default_server == servers['trackcpp']:
        return Tracking.track1turn_trackcpp(lattice, pos)
    else:
        raise Exception('tracking server not defined!')
