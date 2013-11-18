#ifndef _TRACKCPP_H
#define _TRACKCPP_H

#include <iostream>
#include <vector>

#include "Python.h"
#include "../../../trackc++/elements.h"

// auxiliary functions
void trackcpp_read_particles (PyObject *py_particles, std::vector<double>&  v);
void trackcpp_read_lattice   (PyObject *py_lattice,   std::vector<Element>& v);

// exposed functionalities
PyObject*  trackcpp_track1turn(PyObject *Self, PyObject *args);


#endif
