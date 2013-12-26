#include "fieldmapcpp.h"

// MODULE Docstrings
static char module_docstring[]                    = "This a module for loading and interpolating on fieldmaps. It also does runge-kutta integration.";
static char fieldmapcpp_load_docstring[]          = "load(filename)";
static char fieldmapcpp_unload_docstring[]        = "unload(fieldmap_id)";
static char fieldmapcpp_interpolate_docstring[]   = "interpolate(fieldmap_id, pos)";
static char fieldmapcpp_nr_fieldmaps_docstring[]  = "nr_fieldmaps()";
static char fieldmapcpp_clear_docstring[]         = "clear()";
static char fieldmapcpp_error[] = "fieldmap.error";

// MODULE Global variables for dealing with module exceptions
PyObject    *FieldMapCppError;
std::string  FieldMapCppErrorMsg;

// MODULE Interface
static PyMethodDef fieldmapcpp_methods[] = {
	{"load",         (PyCFunction) fieldmapcpp_load_fieldmap,        METH_VARARGS, fieldmapcpp_load_docstring},
	{"unload",       (PyCFunction) fieldmapcpp_unload_fieldmap,      METH_VARARGS, fieldmapcpp_unload_docstring},
	{"interpolate",  (PyCFunction) fieldmapcpp_interpolate_fieldmap, METH_VARARGS, fieldmapcpp_interpolate_docstring},
	{"nr_fieldmaps", (PyCFunction) fieldmapcpp_nr_fieldmaps,         METH_VARARGS, fieldmapcpp_nr_fieldmaps_docstring},
	{"clear",        (PyCFunction) fieldmapcpp_clear,                METH_VARARGS, fieldmapcpp_clear_docstring},
	{NULL, NULL, 0, NULL}
};

// MODULE Initialization routine
PyMODINIT_FUNC initfieldmapcpp(void) {
	PyObject *module = Py_InitModule3("fieldmapcpp", fieldmapcpp_methods, module_docstring);
	if (module == NULL) return;
	FieldMapCppError = PyErr_NewException(fieldmapcpp_error, (PyObject*) NULL, (PyObject*) NULL);
	Py_INCREF(FieldMapCppError);
	PyModule_AddObject(module, "error", FieldMapCppError);
};
