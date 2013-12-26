#include "fieldmapcpp.h"

// Exception object
extern PyObject *FieldMapCppError;
extern std::string FieldMapCppErrorMsg;


int fieldmapcpp_read_pos(PyObject *py_pos, std::vector<Vector3D<double> >& pos) {

	pos.clear();
	int nr_pts = PyList_Size(py_pos);
	//std::cout << nr_pts << std::endl;
	//return 0;

	for(int p=0; p<(nr_pts/3); ++p) {
		PyObject *py_x = PyList_GetItem(py_pos, p*3+0);
		PyObject *py_y = PyList_GetItem(py_pos, p*3+1);
		PyObject *py_z = PyList_GetItem(py_pos, p*3+2);
		Vector3D<double> _pos(PyFloat_AsDouble(py_x), PyFloat_AsDouble(py_y), PyFloat_AsDouble(py_z));
		pos.push_back(_pos);
	}
	return 0;
}
