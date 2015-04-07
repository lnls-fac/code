
import numpy as _numpy
import trackcpp as _trackcpp


class TrackingException(Exception):
    pass


def elementpass(element, pos, accelerator):
    """Track particle(s) through an element.

    Accepts one or multiple particles. In the latter case, a list of particles
    or numpy 2D array (with particle as first index) should be given as input;
    also, outputs get an additional dimension, with particle as first index.

    Keyword arguments:
    element     -- Element object
    pos         -- initial 6D position or list of positions
    accelerator -- Accelerator object

    Returns:
    pos -- 6D position at each element

    Raises TrackingException
    """

    if (type(pos) == list and type(pos[0]) != list or
            type(pos) == _numpy.ndarray and pos.ndim == 1):
        pos = [pos]
        multiple = False
    else:
        multiple = True

    pos_out = []

    for p in pos:
        x = _trackcpp.DoublePos()
        x.rx, x.px = p[0], p[1]
        x.ry, x.py = p[2], p[3]
        x.dl, x.de = p[4], p[5]

        r = _trackcpp.double_track_elementpass(element._e, x, accelerator._a)
        if r > 0:
            raise TrackingException(_trackcpp.string_error_messages[r])

        pos_out.append(_numpy.array([x.rx, x.px, x.ry, x.py, x.dl, x.de]))

    if not multiple:
        pos_out = pos_out[0]
    else:
        pos_out = _numpy.array(pos_out)

    return pos_out


def linepass(accelerator, pos, trajectory=False, offset=0):
    """Track particle(s) along a line.

    Accepts one or multiple particles. In the latter case, a list of particles
    or numpy 2D array (with particle as first index) should be given as input;
    also, outputs get an additional dimension, with particle as first index.

    Keyword arguments:
    accelerator -- Accelerator object
    pos         -- initial 6D position or list of positions
    trajectory  -- True if trajectory should be calculated at each element
                   (default False)
    offset      -- element offset (default 0)

    Returns: (pos, offset, plane)
    pos    -- 6D position at each element
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

    args = _trackcpp.LinePassArgs()
    args.trajectory = trajectory

    pos_out, offset_out, plane_out = [], [], []

    for p in pos:
        args.element_offset = offset
        x0 = _trackcpp.DoublePos()
        x0.rx, x0.px = p[0], p[1]
        x0.ry, x0.py = p[2], p[3]
        x0.dl, x0.de = p[4], p[5]

        x = _trackcpp.CppDoublePosVector()
        r = _trackcpp.track_linepass_wrapper(accelerator._accelerator, x0, x, args)
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
        offset_out.append(args.element_offset)
        plane_out.append(args.lost_plane)

    if not multiple:
        pos_out = pos_out[0]
        offset_out = offset_out[0]
        plane_out = plane_out[0]
    else:
        pos_out = _numpy.array(pos_out)

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

    orbit = _trackcpp.CppDoublePosVector()
    r = _trackcpp.track_findorbit6(accelerator._accelerator, orbit)
    if r > 0:
        raise TrackingException(_trackcpp.string_error_messages[r])

    orbit_out = _numpy.zeros((6, len(orbit)))
    for i in range(len(orbit)):
        orbit_out[:, i] = [
            orbit[i].rx, orbit[i].px,
            orbit[i].ry, orbit[i].py,
            orbit[i].dl, orbit[i].de
        ]

    return orbit_out


def findm66(accelerator):
    """Calculate accumulated 6D transfer matrices.

    Keyword arguments:
    accelerator -- Accelerator object

    Returns:
    matrices -- array of matrices along accelerator elements

    Raises TrackingException
    """

    orbit = _trackcpp.CppDoublePosVector()
    r = _trackcpp.track_findorbit6(accelerator._accelerator, orbit)
    if r > 0:
        raise TrackingException(_trackcpp.string_error_messages[r])

    orbit = _trackcpp.CppDoublePosVector()
    m66 = _trackcpp.CppDoubleMatrixVector()
    r = _trackcpp.track_findm66(accelerator._accelerator, orbit, m66)
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
