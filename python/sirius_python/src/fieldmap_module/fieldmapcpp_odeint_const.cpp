#include "fieldmapcpp.h"

// Exception object
extern PyObject    *FieldMapCppError;
extern std::string  FieldMapCppErrorMsg;


PyObject*  fieldmapcpp_odeint_const(PyObject *self, PyObject *args)
{
	PyObject *py_energy;
	PyObject *py_id;
	PyObject *py_si, *py_sf;
	PyObject *py_nrpts;
	PyObject *py_init_state;

	if (!PyArg_ParseTuple(args, "OOOOOO", &py_id, &py_energy, &py_si, &py_sf, &py_nrpts, &py_init_state))
		return NULL;

	size_t     id = (size_t) PyLong_AsLong(py_id);
	const FieldMap* fieldmap = getfieldmap(id);
	if (fieldmap == NULL) {
		FieldMapCppErrorMsg = "there is no fieldmap corresponding to passed fieldmap_id";
		PyErr_SetString(FieldMapCppError, FieldMapCppErrorMsg.c_str());
		return NULL;
	}

	double energy = PyFloat_AsDouble(py_energy);
	double     si = PyFloat_AsDouble(py_si);
	double     sf = PyFloat_AsDouble(py_sf);
	size_t  nrpts = (size_t) PyLong_AsLong(py_nrpts);
	//std::cout << energy << " " << si << " " << sf << " " << nrpts << std::endl;

	Py_INCREF(py_init_state);
	std::vector<double> init_state;
	fieldmapcpp_read_pos(py_init_state, init_state);
	Py_DECREF(py_init_state);

	std::vector<double> s;
	std::vector<state_type> trajectory;
	boost_integrate_const(energy, *fieldmap, si, sf, nrpts, init_state, s, trajectory);

	PyObject *py_lst  = PyList_New(7*s.size());
	for(size_t i=0; i<s.size(); ++i) {
		PyObject *py_s     = PyFloat_FromDouble(s[i]);
		PyObject *py_x     = PyFloat_FromDouble(trajectory[i][0]);
		PyObject *py_betax = PyFloat_FromDouble(trajectory[i][1]);
		PyObject *py_y     = PyFloat_FromDouble(trajectory[i][2]);
		PyObject *py_betay = PyFloat_FromDouble(trajectory[i][3]);
		PyObject *py_z     = PyFloat_FromDouble(trajectory[i][4]);
		PyObject *py_betaz = PyFloat_FromDouble(trajectory[i][5]);
		PyList_SET_ITEM(py_lst, 7*i+0, py_s);
		PyList_SET_ITEM(py_lst, 7*i+1, py_x);
		PyList_SET_ITEM(py_lst, 7*i+2, py_betax);
		PyList_SET_ITEM(py_lst, 7*i+3, py_y);
		PyList_SET_ITEM(py_lst, 7*i+4, py_betay);
		PyList_SET_ITEM(py_lst, 7*i+5, py_z);
		PyList_SET_ITEM(py_lst, 7*i+6, py_betaz);
	}
	return py_lst;

}
