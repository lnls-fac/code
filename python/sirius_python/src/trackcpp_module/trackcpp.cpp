#include "trackcpp.h"

// MODULE Docstrings
static char module_docstring[]            = "Module for efficiently tracking particles in transport lines and storage rings";
static char trackcpp_linepass_docstring[] = "linepass(the_ring, particles, trajectory)";
static char trackcpp_ringpass_docstring[] = "ringpass(the_ring, particles)";
static char trackcpp_error[] = "trackcpp.error";

// MODULE Global variables for dealing with module exceptions
PyObject    *TrackcppError;
std::string  TrackcppErrorMsg;

// MODULE Interface
static PyMethodDef trackcpp_methods[] = {
	{"linepass", (PyCFunction)trackcpp_linepass, METH_VARARGS, trackcpp_linepass_docstring},
	{"ringpass", (PyCFunction)trackcpp_ringpass, METH_VARARGS, trackcpp_ringpass_docstring},
	{NULL, NULL, 0, NULL}
};

// MODULE Initialization routine
PyMODINIT_FUNC inittrackcpp(void) {
	PyObject *module = Py_InitModule3("trackcpp", trackcpp_methods, module_docstring);
	if (module == NULL) return;
	TrackcppError = PyErr_NewException(trackcpp_error, (PyObject*) NULL, (PyObject*) NULL);
	Py_INCREF(TrackcppError);
	PyModule_AddObject(module, "error", TrackcppError);
};
