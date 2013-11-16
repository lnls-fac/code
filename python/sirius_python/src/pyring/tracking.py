import passmethods
import trackcpp

servers = {
    'pyring'   : 0,
    'trackcpp' : 1,
    'trackmgr' : 2,
}

default_sever = servers['pyring']

class Tracking:

    @staticmethod
    def track1turn_pyring(lattice, pos):
        for element in latice:
            (pm_name, pm_map) = passmethods.PassMethod.dict[element.pass_method]
            pm_map(pos, element)
        return pos

    @staticmethod
    def track1turn_trackcpp(lattice, pos):
        return trackcpp.track1turn(lattice, pos)


def track1turn(latice, pos):
    if default_server == servers['pyring']:
        return Tracking.track1turn_pyring(lattice, pos)
    elif default_sever == servers['trackcpp']:
        return Tracking.track1turn_trackcpp(latice, pos)
    else:
        raise Exception('tracking server not defined!')
