
import numpy as _numpy
import trackcpp as _trackcpp


class TrackingException(Exception):
    pass


def elementpass(element, pos, accelerator):
    """Track particle(s) thouhg an element.

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
        x.rx = p[0]
        x.px = p[1]
        x.ry = p[2]
        x.py = p[3]
        x.dl = p[4]
        x.de = p[5]

        r = _trackcpp.double_track_elementpass(element, x, accelerator)
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

    pos_out = []
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
        r = _trackcpp.track_linepass_wrapper(accelerator, x0, x, args)
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


def ringpass(accelerator, pos, num_turns=1, trajectory=False, offset=0):
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
    args.nr_turns = num_turns
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
        r = _trackcpp.track_ringpass_wrapper(accelerator, x0, x, args)
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


def findorbit6(accelerator):
    """Calculate 6D orbit.

    Accepts one or multiple particles. In the latter case, a list of particles
    or numpy 2D array (with particle as first index) should be given as input;
    also, outputs get an additional dimension, with particle as first index.

    Keyword arguments:
    accelerator -- Accelerator object

    Returns:
    orbit -- 6D position at each element

    Raises TrackingException
    """

    orbit = _trackcpp.CppDoublePosVector()
    r = _trackcpp.track_findorbit6(accelerator, orbit)
    if r > 0:
        raise TrackingException(_trackcpp.string_error_messages[r])

    return orbit
