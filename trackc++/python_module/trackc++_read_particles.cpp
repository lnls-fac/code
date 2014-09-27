#include "trackc++.h"

int trackcpp_read_particles(PyObject *py_particles, std::vector<Pos<double> >& pos) {

	pos.clear();
	int nr_pts = PyList_Size(py_particles);
	//std::cout << "here" << std::endl;
	//std::cout << (nr_pts/6) << std::endl;
	for(int p=0; p<(nr_pts/6); ++p) {
		PyObject *py_rx = PyList_GetItem(py_particles, p*6+0);
		PyObject *py_px = PyList_GetItem(py_particles, p*6+1);
		PyObject *py_ry = PyList_GetItem(py_particles, p*6+2);
		PyObject *py_py = PyList_GetItem(py_particles, p*6+3);
		PyObject *py_de = PyList_GetItem(py_particles, p*6+4);
		PyObject *py_dl = PyList_GetItem(py_particles, p*6+5);
		Pos<double> _pos(
				PyFloat_AsDouble(py_rx), PyFloat_AsDouble(py_px),
				PyFloat_AsDouble(py_ry), PyFloat_AsDouble(py_py),
				PyFloat_AsDouble(py_de), PyFloat_AsDouble(py_dl)
				);
		pos.push_back(_pos);
		//std::cout << p << ": " << _pos.rx << " " << _pos.px << " " << _pos.ry << " " << _pos.py << " " << _pos.de << " " << _pos.dl << std::endl;
	}
	return 0;
}
