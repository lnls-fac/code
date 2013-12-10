#include "trackcpp.h"

// DOCSTRINGS
static char module_docstring[]            = "Module for efficiently tracking particles in transport lines and storage rings";
static char trackcpp_linepass_docstring[] = "linepass(the_ring, particles, trajectory)";
static char trackcpp_ringpass_docstring[] = "ringpass(the_ring, particles)";

static PyMethodDef trackcpp_methods[] = {
	{"linepass", (PyCFunction)trackcpp_linepass, METH_VARARGS, trackcpp_linepass_docstring},
	{"ringpass", (PyCFunction)trackcpp_ringpass, METH_VARARGS, trackcpp_ringpass_docstring},
	{NULL, NULL, 0, NULL}
};

PyObject *TrackcppError;
std::string TrackcppErrorMsg;


PyMODINIT_FUNC inittrackcpp(void) {
	PyObject *m = Py_InitModule3("trackcpp", trackcpp_methods, module_docstring);
	if (m == NULL) return;
	TrackcppError = PyErr_NewException("trackcpp.error", (PyObject*) NULL, (PyObject*) NULL);
	Py_INCREF(TrackcppError);
	PyModule_AddObject(m, "error", TrackcppError);
};
