#!/usr/bin/env python3

import SI_V07.sirius_si as sirius_si
import pyaccel
import matplotlib.pyplot as plt

accelerator = pyaccel.accelerator.Accelerator()
accelerator.energy  = 3e9
accelerator.lattice = sirius_si.lattice()
accelerator.harmonic_number = sirius_si.harmonic_number
accelerator.cavity_on = False
accelerator.radiation_on = False
accelerator.vchamber_on = False
the_ring = accelerator.lattice


pos = [0.001,0,0,0,0,0]
num_turns, trajectory, offset = 512, True, 0
pos, turn, offset, plane = pyaccel.tracking.ringpass(accelerator, pos, num_turns, trajectory, offset)
x,xl = pos[0,:], pos[1,:]
plt.plot(x,xl,'o')

idx = pyaccel.lattice.findcells(the_ring, 'fam_name', 'cav')
the_ring[idx[0]].frequency = 0

pos = [0.001,0,0,0,0,0]
num_turns, trajectory, offset = 512, True, 0
pos, turn, offset, plane = pyaccel.tracking.ringpass(accelerator, pos, num_turns, trajectory, offset)
x,xl = pos[0,:], pos[1,:]
plt.plot(x,xl,'o')


plt.show()
