#ifndef _FIELDMAPCPP_H
#define _FIELDMAPCPP_H

#include <iostream>
#include <vector>
#include <sstream>
#include <string>

#include "Python.h"

#include "../../../../fieldmap/API.h"

// auxiliary functions
int fieldmapcpp_read_pos       (PyObject *py_particles, std::vector<Vector3D<double> >&  pos);

// exposed functionalities
PyObject*  fieldmapcpp_load_fieldmap        (PyObject *Self, PyObject *args);
PyObject*  fieldmapcpp_unload_fieldmap      (PyObject *Self, PyObject *args);
PyObject*  fieldmapcpp_interpolate_fieldmap (PyObject *Self, PyObject *args);
PyObject*  fieldmapcpp_nr_fieldmaps         (PyObject *Self, PyObject *args);
PyObject*  fieldmapcpp_clear                (PyObject *Self, PyObject *args);

#endif
