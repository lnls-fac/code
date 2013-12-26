// TRACKCPP
// ========
// Author: 		Ximenes R. Resende
// email:  		xresende@gmail.com, ximenes.resende@lnls.br
// affiliation:	LNLS - Laboratorio Nacional de Luz Sincrotron
// Date: 		Mon Dec 23 16:45:42 BRST 2013


#include "fieldmapcpp.h"

// Exception object
extern PyObject    *FieldMapCppError;
extern std::string  FieldMapCppMsg;


PyObject*  fieldmapcpp_unload_fieldmap(PyObject *self, PyObject *args) {

	PyObject *py_id;
	if (!PyArg_ParseTuple(args, "O", &py_id))
		return NULL;
	Py_INCREF(py_id);
	size_t id = PyInt_AsSsize_t(py_id);
	Py_DECREF(py_id);

	// unloads fieldmap into global vector
	unload_fieldmap(id);

	Py_RETURN_NONE;

}

