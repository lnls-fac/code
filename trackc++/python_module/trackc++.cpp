#include "trackc++.h"

// MODULE Docstrings
static char module_docstring[]            = "Module for efficiently tracking particles in transport lines and storage rings";
static char trackcpp_linepass_docstring[] = "linepass(line, particles, trajectory, element_offset)";
static char trackcpp_ringpass_docstring[] = "ringpass(ring, particles, nr_turns, element_offset)";
static char trackcpp_findm66_docstring[]  = "findm66(line, closed_orbit)";
static char trackcpp_error[] = "trackcpp.error";

// MODULE Global variables for dealing with module exceptions
PyObject    *TrackcppError;
std::string  TrackcppErrorMsg;

// MODULE Interface
static PyMethodDef trackcpp_methods[] = {
	{"linepass", (PyCFunction)trackcpp_linepass, METH_VARARGS, trackcpp_linepass_docstring},
	{"ringpass", (PyCFunction)trackcpp_ringpass, METH_VARARGS, trackcpp_ringpass_docstring},
	{"findm66",  (PyCFunction)trackcpp_findm66, METH_VARARGS, trackcpp_findm66_docstring},
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
