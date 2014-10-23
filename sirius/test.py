import sirius.bo.lattices.v900_m0 as v900_m0
import pyaccel.lattice as latt


the_ring = v900_m0.create_lattice(energy=0.15)
b = latt.findcells(the_ring, 'fam_name', 'b')
lengths = latt.getcellstruct(lattice=the_ring, attribute_name='length', indices=b[:14])
s = latt.findspos(the_ring)

import matplotlib.pyplot as plt
plt.plot(s)
plt.show()
