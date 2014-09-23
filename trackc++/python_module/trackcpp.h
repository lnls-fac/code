#ifndef _TRACKCPP_H
#define _TRACKCPP_H

#include <iostream>
#include <vector>
#include <sstream>
#include <string>

#include "Python.h"

#include "../../../trackc++/auxiliary.h"
#include "../../../trackc++/pos.h"
#include "../../../trackc++/elements.h"
#include "../../../trackc++/passmethods.h"
#include "../../../trackc++/lattice.h"
#include "../../../trackc++/tracking.h"

// auxiliary functions
int trackcpp_read_particles (PyObject *py_particles, std::vector<Pos<double> >&  pos);
int trackcpp_read_lattice   (PyObject *py_lattice,   std::vector<Element>& pos);

// exposed functionalities
PyObject*  trackcpp_linepass (PyObject *Self, PyObject *args);
PyObject*  trackcpp_ringpass (PyObject *Self, PyObject *args);
PyObject*  trackcpp_findm66  (PyObject *Self, PyObject *args);

#endif
