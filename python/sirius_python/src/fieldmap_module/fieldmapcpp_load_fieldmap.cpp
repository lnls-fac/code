#include "fieldmapcpp.h"

// Exception object
extern PyObject    *FieldMapCppError;
extern std::string  FieldMapCppErrorMsg;


PyObject*  fieldmapcpp_load_fieldmap(PyObject *self, PyObject *args) {

	PyObject *py_filename;
	if (!PyArg_ParseTuple(args, "O", &py_filename))
		return NULL;
	Py_INCREF(py_filename);
	std::string filename = PyString_AS_STRING(py_filename);
	//std::cout << filename << std::endl;
	Py_DECREF(py_filename);

	// loads fieldmap into global vector
	try {
		size_t id, nx, nz;
		double x_min, x_max, z_min, z_max;
		load_fieldmap(filename, id, nx, x_min, x_max, nz, z_min, z_max);
		PyObject *py_lst  = PyList_New(7);
		PyObject *py_id   = PyInt_FromSize_t(id);      PyList_SET_ITEM(py_lst, 0, py_id);
		PyObject *py_nx   = PyInt_FromSize_t(nx);      PyList_SET_ITEM(py_lst, 1, py_nx);
		PyObject *py_xmin = PyFloat_FromDouble(x_min); PyList_SET_ITEM(py_lst, 2, py_xmin);
		PyObject *py_xmax = PyFloat_FromDouble(x_max); PyList_SET_ITEM(py_lst, 3, py_xmax);
		PyObject *py_nz   = PyInt_FromSize_t(nz);      PyList_SET_ITEM(py_lst, 4, py_nz);
		PyObject *py_zmin = PyFloat_FromDouble(z_min); PyList_SET_ITEM(py_lst, 5, py_zmin);
		PyObject *py_zmax = PyFloat_FromDouble(z_max); PyList_SET_ITEM(py_lst, 6, py_zmax);
		return py_lst;

	} catch (...) {
		FieldMapCppErrorMsg = "could not find fieldmap file";
		PyErr_SetString(FieldMapCppError, FieldMapCppErrorMsg.c_str());
		return NULL;
	}	

}

