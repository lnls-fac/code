#include "trackcpp.h"

void trackcpp_read_particles(PyObject *py_particles, std::vector<Pos<double> >& pos) {

	pos.clear();
	int nr_pts = PyList_Size(py_particles);
	for(int i=0; i<(nr_pts/6); ++i) {
		PyObject *py_rx = PyList_GetItem(py_particles, i*6+0);
		PyObject *py_px = PyList_GetItem(py_particles, i*6+1);
		PyObject *py_ry = PyList_GetItem(py_particles, i*6+2);
		PyObject *py_py = PyList_GetItem(py_particles, i*6+3);
		PyObject *py_de = PyList_GetItem(py_particles, i*6+4);
		PyObject *py_dl = PyList_GetItem(py_particles, i*6+5);
		Pos<double> p(
				PyFloat_AsDouble(py_rx), PyFloat_AsDouble(py_px),
				PyFloat_AsDouble(py_ry), PyFloat_AsDouble(py_py),
				PyFloat_AsDouble(py_de), PyFloat_AsDouble(py_dl)
				);
		pos.push_back(p);
		//std::cout << i << " " << pos << std::endl;
	}

}
