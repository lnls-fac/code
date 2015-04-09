import numpy as _numpy
import trackcpp as _trackcpp
import pyaccel.accelerator


class TrackingException(Exception):
    pass

def elementpass(element, pos, **kwargs):

    """Track particle(s) through an element.

    Accepts one or multiple particles initial positions. In the latter case,
    a list of particles or numpy 2D array (with particle as second index)
    should be given as input; also, outputs get an additional dimension,
    with particle as second index.

    Keyword arguments:
    element         -- Element object
    pos             -- initial 6D position or list of positions
    energy          -- energy of the beam [eV]
    harmonic_number -- harmonic number of the lattice
    cavity_on       -- cavity on state (True/False)
    radiation_on    -- radiation on state (True/False)
    vchamber_on     -- vacuum chamber on state (True/False)

    Returns:
    pos_out -- a numpy array with tracked 6D position(s) of the particle(s)

    Raises TrackingException
    """

    # checks if all necessary arguments have been passed
    keys_needed = ['energy','harmonic_number','cavity_on','radiation_on','vchamber_on']
    for key in keys_needed:
        if key not in kwargs:
            raise TrackingException("missing '" + key + "' argument'")

    # creates accelerator for tracking
    accelerator = pyaccel.accelerator.Accelerator(**kwargs)

    # checks whether single or multiple particles
    return_ndarray = True
    if isinstance(pos, (list,tuple)):
        if isinstance(pos[0], (list,tuple)):
            pos = _numpy.transpose(_numpy.array(pos))
        else:
            pos = _numpy.transpose(_numpy.array(pos,ndmin=2))
            return_ndarray = False

    # tracks through the list of pos
    pos_out = _numpy.zeros(pos.shape)
    for i in range(pos.shape[1]):
        p_in = _Numpy2CppDoublePos(pos[:,i])
        r = _trackcpp.track_elementpass_wrapper(element._e,
                                                p_in, accelerator._accelerator)
        if r > 0:
            raise TrackingException(_trackcpp.string_error_messages[r])
        pos_out[:,i] = (p_in.rx, p_in.px, p_in.ry, p_in.py, p_in.dl, p_in.de)

    # returns tracking data
    if pos_out.shape[1] == 1 and not return_ndarray:
        return pos_out[:,0]
    else:
        return pos_out


def linepass(accelerator, pos, indices=None, offset=0):
    """Track particle(s) along a line.

    Accepts one or multiple particles initial positions. In the latter case,
    a list of particles or numpy 2D array (with particle as second index)
    should be given as input; also, outputs get an additional dimension,
    with particle as second index.

    Keyword arguments:
    accelerator -- Accelerator object
    pos         -- initial 6D position or list of positions
    indices     -- list of indices corresponding to accelerator elements at
                   whose exits the tracked particles positions are to be
                   stored; string 'all' corresponds to selecting all elements.
    offset      -- element offset (default 0)

    Returns: (pos, offset, plane)
    pos    -- 6D position for each particle at each element exit
    offset -- last element offset
    plane  -- plane where particle was lost

    Raises TrackingException
    """

    # checks whether single or multiple particles
    return_ndarray = True
    if isinstance(pos, (list,tuple)):
        if isinstance(pos[0], (list,tuple)):
            pos = _numpy.transpose(_numpy.array(pos))
        else:
            pos = _numpy.transpose(_numpy.array(pos,ndmin=2))
            return_ndarray = False

    if indices == 'all':
        indices = range(len(accelerator))

    args = _trackcpp.LinePassArgs()
    if indices is None:
        args.trajectory = False
        pos_out = _numpy.zeros((6,pos.shape[1]))
    else:
        args.trajectory = True
        pos_out = _numpy.zeros((len(indices),6,pos.shape[1]))

    offset_out, plane_out = [], []
    for i in range(pos.shape[1]):
        args.element_offset = offset
        p_in = _Numpy2CppDoublePos(pos[:,i])
        p_out = _trackcpp.CppDoublePosVector()
        r = _trackcpp.track_linepass_wrapper(accelerator._accelerator, p_in, p_out, args)
        if r > 0:
            raise TrackingException(_trackcpp.string_error_messages[r])
        if indices is None:
            pos_out[:,i] = _CppDoublePos2Numpy(p_out[0])
        else:
            for j in range(len(indices)):
                pos_out[j,:,i] = _CppDoublePos2Numpy(p_out[1+indices[j]])
        offset_out.append(args.element_offset)
        plane_out.append(args.lost_plane)

    if len(offset_out) == 1 and not return_ndarray:
        pos_out = pos_out[:,0]
        offset_out = offset_out[0]
        plane_out = plane_out[0]

    return pos_out, offset_out, plane_out


def ringpass(accelerator, pos, nr_turns=1, trajectory=False, offset=0):
    """Track particle(s) along a ring.

    Accepts one or multiple particles. In the latter case, a list of particles
    or numpy 2D array (with particle as first index) should be given as input;
    also, outputs get an additional dimension, with particle as first index.

    Keyword arguments:
    accelerator -- Accelerator object
    pos         -- initial 6D position or list of positions
    num_turns   -- number of turns (default 1)
    trajectory  -- True if trajectory should be calculated at each element
                   (default False)
    offset      -- element offset (default 0)

    Returns: (pos, turn, offset, plane)
    pos    -- 6D position at each element
    turn   -- last turn number
    offset -- last element offset
    plane  -- plane where particle was lost

    Raises TrackingException
    """

    if (type(pos) == list and type(pos[0]) != list or
            type(pos) == _numpy.ndarray and pos.ndim == 1):
        pos = [pos]
        multiple = False
    else:
        multiple = True

    args = _trackcpp.RingPassArgs()
    args.nr_turns = nr_turns
    args.trajectory = trajectory

    pos_out = []
    turn_out = []
    offset_out = []
    plane_out = []

    for p in pos:
        args.element_offset = offset
        x0 = _trackcpp.DoublePos()
        x0.rx = p[0]
        x0.px = p[1]
        x0.ry = p[2]
        x0.py = p[3]
        x0.dl = p[4]
        x0.de = p[5]

        x = _trackcpp.CppDoublePosVector()
        r = _trackcpp.track_ringpass_wrapper(accelerator._accelerator, x0, x, args)
        if r > 0:
            raise TrackingException(_trackcpp.string_error_messages[r])

        x_out = _numpy.zeros((6, len(x)))
        for i in range(len(x)):
            x_out[:, i] = [
                x[i].rx, x[i].px,
                x[i].ry, x[i].py,
                x[i].dl, x[i].de
            ]

        pos_out.append(x_out)
        turn_out.append(args.lost_turn)
        offset_out.append(args.element_offset)
        plane_out.append(args.lost_plane)

    if not multiple:
        pos_out = pos_out[0]
        turn_out = turn_out[0]
        offset_out = offset_out[0]
        plane_out = plane_out[0]
    else:
        pos_out = _numpy.array(pos_out)

    return pos_out, turn_out, offset_out, plane_out


def set4dtracking(accelerator):
    accelerator.cavity_on = False
    accelerator.radiation_on = False


def set6dtracking(accelerator):
    accelerator.cavity_on = True
    accelerator.radiation_on = True


def findorbit6(accelerator, indices=None):
    """Calculate 6D orbit closed-orbit.

    Accepts an optional list of indices of ring elements where closed-orbit
    coordinates are to be returned. If this argument is not passed closed-orbit
    positions are returned at the start of every element.

    Keyword arguments:
    accelerator -- Accelerator object

    Returns:
    orbit -- 6D position at elements

    Raises TrackingException
    """

    closed_orbit = _trackcpp.CppDoublePosVector()
    r = _trackcpp.track_findorbit6(accelerator._accelerator, closed_orbit)
    if r > 0:
        raise TrackingException(_trackcpp.string_error_messages[r])

    closed_orbit = _CppDoublePosVector2Numpy(closed_orbit, indices)
    return closed_orbit


def findm66(accelerator, closed_orbit = None):
    """Calculate accumulatep_in = _trackcpp.DoublePos()
        p_in.rx,p_in.px,p_in.ry,p_in.py,p_in.dl,p_in.de = pos[:,i]
    matrices -- array of matrices along accelerator elements

    Raises TrackingException
    """
    if closed_orbit is None:
        closed_orbit = _trackcpp.CppDoublePosVector()
        r = _trackcpp.track_findorbit6(accelerator._accelerator, closed_orbit)
        if r > 0:
            raise TrackingException(_trackcpp.string_error_messages[r])
    else:
        if closed_orbit.shape[1] != len(accelerator):
            closed_orbit = _trackcpp.CppDoublePosVector()

    m66 = _trackcpp.CppDoubleMatrixVector()
    r = _trackcpp.track_findm66(accelerator._accelerator, closed_orbit, m66)
    if r > 0:
        raise TrackingException(_trackcpp.string_error_messages[r])

    m66_out = []
    for i in range(len(m66)):
        m = _numpy.zeros((6,6))
        for r in range(6):
            for c in range(6):
                m[r,c] = m66[i][r][c]
        m66_out.append(m)

    return m66_out


def _Numpy2CppDoublePos(p_in):
    p_out = _trackcpp.CppDoublePos()
    p_out.rx, p_out.px = float(p_in[0]), float(p_in[1])
    p_out.ry, p_out.py = float(p_in[2]), float(p_in[3])
    p_out.dl, p_out.de = float(p_in[4]), float(p_in[5])
    return p_out

def _CppDoublePos2Numpy(p_in):
    return (p_in.rx,p_in.px,p_in.ry,p_in.py,p_in.dl,p_in.de)

def _CppDoublePosVector2Numpy(orbit, indices = None):
    if indices is None:
        indices = range(len(orbit))
    elif isinstance(indices,int):
        indices = [indices]
    orbit_out = _numpy.zeros((6, len(indices)))
    for i in range(len(indices)):
        orbit_out[:, i] = [
            orbit[indices[i]].rx, orbit[indices[i]].px,
            orbit[indices[i]].ry, orbit[indices[i]].py,
            orbit[indices[i]].dl, orbit[indices[i]].de
        ]
    return orbit_out

def _Numpy2CppDoublePosVector(orbit):
    orbit_out = _trackcpp.CppDoublePosVector()
    for i in range(orbit.shape[1]):
        orbit_out.push_back(_trackcpp.CppDoublePos(
            orbit[0,i], orbit[1,i],
            orbit[2,i], orbit[3,i],
            orbit[4,i], orbit[5,i]))
    return orbit_out
