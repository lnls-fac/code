#include "fieldmapcpp.h"

// Exception object
extern PyObject    *FieldMapCppError;
extern std::string  FieldMapCppErrorMsg;

PyObject*  fieldmapcpp_nr_fieldmaps(PyObject *self, PyObject *args) {

	size_t nr = nr_fieldmaps();
	PyObject *py_nr   = PyInt_FromSize_t(nr);
	return py_nr;

}


