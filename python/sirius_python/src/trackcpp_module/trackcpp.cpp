#include "trackcpp.h"

// DOCSTRINGS
static char module_docstring[]              = "Module for efficiently tracking particles in transport lines and storage rings";
static char trackcpp_track1turn_docstring[] = "track1turn(the_ring, pos)";

static PyMethodDef trackcpp_methods[] = {
	{"track1turn", (PyCFunction)trackcpp_track1turn, METH_VARARGS, trackcpp_track1turn_docstring},
	{NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC inittrackcpp(void) {
	Py_InitModule3("trackcpp", trackcpp_methods, module_docstring);
};
