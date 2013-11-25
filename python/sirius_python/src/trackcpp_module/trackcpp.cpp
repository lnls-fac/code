#include "trackcpp.h"

// DOCSTRINGS
static char module_docstring[]              = "Module for efficiently tracking particles in transport lines and storage rings";
static char trackcpp_track1turn_docstring[]  = "track1turn(the_ring, pos, trajectory)";
static char trackcpp_tracknturns_docstring[] = "tracknturns(the_ring, pos, turn_by_turn, trajectory)";

static PyMethodDef trackcpp_methods[] = {
	{"track1turn",  (PyCFunction)trackcpp_track1turn,  METH_VARARGS, trackcpp_track1turn_docstring},
	{"tracknturns", (PyCFunction)trackcpp_tracknturns, METH_VARARGS, trackcpp_tracknturns_docstring},
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
