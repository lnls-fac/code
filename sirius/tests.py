#!/usr/bin/env python3

import sirius.SI_V07 as sirius
import pyaccel
import matplotlib.pyplot as plt

def test_plot_phase_space():

    # creates accelerate and inits its lattice
    accelerator = sirius.create_accelerator(cavity_on=False,radiation_on=False,vchamber_on=True)

    # aux. parameters and symbols
    the_ring = accelerator.lattice
    num_turns, trajectory, offset = 512, True, 0

    # calcs phase space at MIA
    pos = [0.001,0,0,0,0,0]
    traj, turn, offset, plane = pyaccel.tracking.ringpass(accelerator, pos, num_turns, trajectory, offset)
    plt.plot(traj[0,:],traj[1,:],'o')

    # propagates from MIA to MIB
    traj, offset, plane = pyaccel.tracking.linepass(accelerator, pos, trajectory, offset)
    idx = pyaccel.lattice.findcells(the_ring, 'fam_name', 'mib')

    # calcs phase space at MIB
    pos = traj[:,idx[0]]
    traj, turn, offset, plane = pyaccel.tracking.ringpass(accelerator, pos, num_turns, trajectory, offset=idx[0])
    plt.plot(traj[0,:],traj[1,:],'o')

    plt.show()

def test_findorbit6():

    # creates accelerate and inits its lattice
    accelerator = sirius.create_accelerator(cavity_on=True,radiation_on=True,vchamber_on=True)

    # finds 6d closed-orbit
    orbit = pyaccel.tracking.findorbit6(accelerator)

    # plots orbit at BPMs
    bpms = pyaccel.lattice.findcells(accelerator.lattice, 'fam_name', 'bpm')
    pos = pyaccel.lattice.findspos(accelerator.lattice)
    plt.plot(pos[bpms], orbit[0,bpms])
    plt.show()

test_plot_phase_space()
#test_findorbit6()
