#include "trackcpp.h"

void trackcpp_read_lattice(PyObject *py_lattice, std::vector<Element>& v) {

	v.clear();
	int nr_elements = PyList_Size(py_lattice);
	for(int i=0; i<nr_elements; ++i) {
		PyObject *py_element = PyList_GetItem(py_lattice, i);

		std::string fam_name;
		if (PyObject_HasAttrString(py_element, "fam_name")) {
			PyObject *py_attr = PyObject_GetAttrString(py_element, "fam_name");
			if (py_attr != NULL) {
				fam_name = PyString_AS_STRING(py_attr);
				Py_DECREF(py_attr);
			}
		}
		double length = 0.0;
		if (PyObject_HasAttrString(py_element, "length")) {
			PyObject *py_attr = PyObject_GetAttrString(py_element, "length");
			if (py_attr != NULL) {
				length = PyFloat_AsDouble(py_attr);
				Py_DECREF(py_attr);
			}
		}
		double angle = 0.0;
		if (PyObject_HasAttrString(py_element, "angle")) {
			PyObject *py_attr = PyObject_GetAttrString(py_element, "angle");
			if (py_attr != NULL) {
				angle = PyFloat_AsDouble(py_attr);
				Py_DECREF(py_attr);
			}
		}

		Element el = Element(fam_name, length);
		el.angle = angle;
		v.push_back(el);
		std::cout << i << ": " << el << std::endl;

	}
}
