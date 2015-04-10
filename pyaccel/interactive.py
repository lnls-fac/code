
import numpy as np
import matplotlib.pyplot as plt
import pyaccel.elements
import pyaccel.accelerator
import pyaccel.lattice
import pyaccel.tracking
import pyaccel.optics
import sirius.SI_V07 as sirius_si


marker = pyaccel.elements.marker
bpm = pyaccel.elements.bpm
drift = pyaccel.elements.drift
hcorrector = pyaccel.elements.hcorrector
vcorrector = pyaccel.elements.vcorrector
corrector = pyaccel.elements.corrector
rbend = pyaccel.elements.rbend
quadrupole = pyaccel.elements.quadrupole
sextupole = pyaccel.elements.sextupole
rfcavity = pyaccel.elements.rfcavity

accelerator = pyaccel.accelerator.Accelerator

lengthlat = pyaccel.lattice.lengthlat
findspos = pyaccel.lattice.findspos
findcells = pyaccel.lattice.findcells
getcellstruct = pyaccel.lattice.getcellstruct
setcellstruct = pyaccel.lattice.setcellstruct
finddict = pyaccel.lattice.finddict
get_rf_frequency = pyaccel.lattice.get_rf_frequency

elementpass = pyaccel.tracking.elementpass
linepass = pyaccel.tracking.linepass
ringpass = pyaccel.tracking.ringpass
set4dtracking = pyaccel.tracking.set4dtracking
set6dtracking = pyaccel.tracking.set6dtracking
findorbit6 = pyaccel.tracking.findorbit6
findm66 = pyaccel.tracking.findm66

create_accelerator = sirius_si.create_accelerator

__all__ = [
        'np',
        'plt',
        'marker',
        'bpm',
        'drift',
        'hcorrector',
        'vcorrector',
        'corrector',
        'rbend',
        'quadrupole',
        'sextupole',
        'rfcavity',
        'accelerator',
        'lengthlat',
        'findspos',
        'findcells',
        'getcellstruct',
        'setcellstruct',
        'finddict',
        'get_rf_frequency',
        'elementpass',
        'linepass',
        'ringpass',
        'set4dtracking',
        'set6dtracking',
        'findorbit6',
        'findm66',
        'create_accelerator'
]
