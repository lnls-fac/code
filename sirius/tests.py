#!/usr/bin/env python3

import sirius.SI_V07 as sirius
import pyaccel
import matplotlib.pyplot as plt

# creates accelerate and inits its lattice
the_ring = sirius.create_accelerator()

accelerator.lattice = pyaccel.lattice.Lattice(elements=sirius.create_lattice())
#
# # global tracking parameters
# accelerator.cavity_on = False
# accelerator.radiation_on = False
# accelerator.vchamber_on = False

# # aux. parameters and symbols
# the_ring = accelerator.lattice
# num_turns, trajectory, offset = 512, True, 0
#
# # calcs phase space at MIA
# pos = [0.001,0,0,0,0,0]
# traj, turn, offset, plane = pyaccel.tracking.ringpass(accelerator, pos, num_turns, trajectory, offset)
# plt.plot(traj[0,:],traj[1,:],'o')
#
# # propagates from MIA to MIB
# traj, offset, plane = pyaccel.tracking.linepass(accelerator, pos, trajectory, offset)
# idx = pyaccel.lattice.findcells(the_ring, 'fam_name', 'mib')
#
# # calcs phase space at MIB
# pos = traj[:,idx[0]]
# traj, turn, offset, plane = pyaccel.tracking.ringpass(accelerator, pos, num_turns, trajectory, offset=idx[0])
# plt.plot(traj[0,:],traj[1,:],'o')
#
# plt.show()
