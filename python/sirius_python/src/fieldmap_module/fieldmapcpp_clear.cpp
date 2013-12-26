#include "fieldmapcpp.h"

// Exception object
extern PyObject    *FieldMapCppError;
extern std::string  FieldMapCppErrorMsg;


PyObject*  fieldmapcpp_clear(PyObject *self, PyObject *args) {

	clear();
	Py_RETURN_NONE;

}
