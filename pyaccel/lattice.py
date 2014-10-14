
import trackcpp as _trackcpp


class Lattice:

    def __init__(self, lattice):
        self._lattice = _trackcpp.cppElementVector()
        for elem in lattice:
            self._lattice.push_back(elem._elem)
