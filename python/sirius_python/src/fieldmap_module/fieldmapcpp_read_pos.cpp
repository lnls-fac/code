#include "fieldmapcpp.h"

// Exception object
extern PyObject *FieldMapCppError;
extern std::string FieldMapCppErrorMsg;


int fieldmapcpp_read_pos(PyObject *py_pos, std::vector<double>& pos) {

	pos.clear();
	int nr_pts = PyList_Size(py_pos);
	//std::cout << nr_pts << std::endl;
	//return 0;

	for(int p=0; p<nr_pts; ++p) {
		PyObject *py_value = PyList_GetItem(py_pos, p);
		double _pos = PyFloat_AsDouble(py_value);
		pos.push_back(_pos);
	}
	return 0;
}
