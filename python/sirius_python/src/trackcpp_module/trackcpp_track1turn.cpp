#include "trackcpp.h"

PyObject*  trackcpp_track1turn(PyObject *self, PyObject *args) {

	PyObject *py_lattice, *py_pos;
	if (!PyArg_ParseTuple(args, "OO", &py_lattice, &py_pos))
		return NULL;

	Py_INCREF(py_lattice);
	Py_INCREF(py_pos);

	std::vector<double> v;
	trackcpp_read_particles(py_pos, v);

	std::vector<Element> lattice;
	trackcpp_read_lattice(py_lattice, lattice);

	Py_DECREF(py_lattice);
	Py_DECREF(py_pos);

	PyObject *py_ret = Py_BuildValue("i", 13);
	return py_ret;

}
