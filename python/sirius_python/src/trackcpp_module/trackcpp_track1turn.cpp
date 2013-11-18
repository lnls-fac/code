#include "trackcpp.h"

// Exception object
extern PyObject *TrackcppError;
extern std::string TrackcppErrorMsg;

PyObject*  trackcpp_track1turn(PyObject *self, PyObject *args) {

	PyObject *py_lattice, *py_pos;
	if (!PyArg_ParseTuple(args, "OO", &py_lattice, &py_pos))
		return NULL;

	Py_INCREF(py_lattice);
	Py_INCREF(py_pos);

	// reads pyring particles coordinates in phase space into trackc++ vector
	std::vector<Pos<double> > pos;
	trackcpp_read_particles(py_pos, pos);

	// reads pyring lattice into trackc++ lattice
	std::vector<Element> lattice;
	trackcpp_read_lattice(py_lattice, lattice);

	// Does tracking
	int element_idx = -1;
	Status::type ret = track1turn(lattice, pos, &element_idx);
	if (ret != Status::success) {
		if (ret == Status::passmethod_not_defined) {
			//std::string str = "Passmethod '" + pm_dict[lattice[element_idx].pass_method] + "' in element #" + std::to_string(element_idx) + " not defined";
			TrackcppErrorMsg = "teste1";
		}
		if (ret == Status::passmethod_not_implemented) {
			//std::string str = "Passmethod '' in element #" + std::to_string(element_idx) + " not implemented";
			//PyErr_SetString(TrackcppError, str.c_str());
			std::string pmname = pm_dict[lattice[element_idx].pass_method];
			TrackcppErrorMsg = "Passmethod '" + pmname + "' in element #" + std::to_string(element_idx) + " not implemented";
		}
		PyErr_SetString(TrackcppError, TrackcppErrorMsg.c_str());
		Py_DECREF(py_lattice);
		Py_DECREF(py_pos);
		return NULL;
	}

	Py_DECREF(py_lattice);
	Py_DECREF(py_pos);

	PyObject *py_ret = Py_BuildValue("i", 13);
	return py_ret;

}
