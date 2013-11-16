#include "trackcpp.h"

void trackcpp_read_particles(PyObject *py_particles, std::vector<double>& v) {

	v.clear();
	int nr_pts = PyList_Size(py_particles);
	for(int i=0; i<nr_pts; ++i) {
		PyObject *py_item = PyList_GetItem(py_particles, i);
		double pos = PyFloat_AsDouble(py_item);
		v.push_back(pos);
		//std::cout << i << " " << pos << std::endl;
	}

}
