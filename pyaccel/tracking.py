
import numpy
import trackcpp as _trackcpp


def linepass(accelerator, pos, trajectory=False, offset=0):
    """Track particle(s) through a line.

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
    """

    if (type(pos) == list and type(pos[0]) != list or
            type(pos) == numpy.ndarray and pos.ndim == 1):
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

        x = _trackcpp.CppPosVector()
        r = _trackcpp.track_linepass_wrapper(accelerator, x0, x, args)

        x_out = numpy.zeros((6, len(x)))
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
        pos_out = numpy.array(pos_out)

    return pos_out, offset_out, plane_out


def ringpass(accelerator, pos, num_turns=1, trajectory=False, offset=0):
    """Track particle(s) through a ring.

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
    """

    if (type(pos) == list and type(pos[0]) != list or
            type(pos) == numpy.ndarray and pos.ndim == 1):
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

        x = _trackcpp.CppPosVector()
        r = _trackcpp.track_ringpass_wrapper(accelerator, x0, x, args)

        x_out = numpy.zeros((6, len(x)))
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
        pos_out = numpy.array(pos_out)

    return pos_out, turn_out, offset_out, plane_out
