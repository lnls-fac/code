#include "trackcpp.h"

// Exception object
extern PyObject *TrackcppError;
extern std::string TrackcppErrorMsg;

PyObject*  trackcpp_findm66(PyObject *self, PyObject *args) {

	PyObject *py_lattice, *py_closed_orbit;
	if (!PyArg_ParseTuple(args, "OO", &py_lattice, &py_closed_orbit))
		return NULL;

	Py_INCREF(py_lattice);
	Py_INCREF(py_closed_orbit);

	// reads pyring lattice into trackc++ lattice
	std::vector<Element> lattice;
	if (trackcpp_read_lattice(py_lattice, lattice)) {
		TrackcppErrorMsg = "read_lattice: error";
		PyErr_SetString(TrackcppError, TrackcppErrorMsg.c_str());
		Py_DECREF(py_lattice);
		Py_DECREF(py_closed_orbit);
		return NULL;
	}
	//Py_RETURN_NONE;

	// reads pyring closed orbit into trackc++ vector
	std::vector<Pos<double> > closed_orbit;
	if (trackcpp_read_particles(py_closed_orbit, closed_orbit)) {
		TrackcppErrorMsg = "read_particles(closed_orbit): error";
		PyErr_SetString(TrackcppError, TrackcppErrorMsg.c_str());
		Py_DECREF(py_lattice);
		Py_DECREF(py_closed_orbit);
		return NULL;
	}
	//Py_RETURN_NONE;

	if (closed_orbit.size() != lattice.size()) {
		TrackcppErrorMsg = "inconsistent number of elements in 'closed_orbit' and 'line' parameters";
		PyErr_SetString(TrackcppError, TrackcppErrorMsg.c_str());
		Py_DECREF(py_lattice);
		Py_DECREF(py_closed_orbit);
		return NULL;
	}

	// allocates memory for the 6x6 transfer matrices
	std::vector<double*> m66;
	for (unsigned int i = 0; i<lattice.size(); ++i) {
		m66.push_back(new double[36]);
	}

	if (findm66 (lattice, closed_orbit, m66) != Status::success) {
		TrackcppErrorMsg = "findm66: error";
		PyErr_SetString(TrackcppError, TrackcppErrorMsg.c_str());
		Py_DECREF(py_lattice);
		Py_DECREF(py_closed_orbit);
		for(unsigned int i=0; i<m66.size(); ++i) delete m66[i];
		return NULL;
	}


	Py_DECREF(py_lattice);
	Py_DECREF(py_closed_orbit);

	// Fills a Python List with all transfer matrices
	PyObject *lst = PyList_New(36*m66.size());
	if (!lst) {
		TrackcppErrorMsg = "findm66: error allocating memory for result";
		PyErr_SetString(TrackcppError, TrackcppErrorMsg.c_str());
		for(unsigned int i=0; i<m66.size(); ++i) delete m66[i];
		return NULL;
	}
	for (unsigned int i = 0; i < m66.size(); i++) {
		for (unsigned int e=0; e < 36; ++e) {
			PyObject *py_element = PyFloat_FromDouble(m66[i][e]);
			if (!py_element) {
				TrackcppErrorMsg = "findm66: could not create a pyFloat object";
				PyErr_SetString(TrackcppError, TrackcppErrorMsg.c_str());
				for(unsigned int i=0; i<m66.size(); ++i) delete m66[i];
				Py_DECREF(lst);
				return NULL;
			}
			PyList_SET_ITEM(lst, i*36+e, py_element);   // reference to num stolen
		}
	}

	return lst;

}
