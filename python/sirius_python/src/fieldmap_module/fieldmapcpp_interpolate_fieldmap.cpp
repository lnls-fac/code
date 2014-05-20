#include "fieldmapcpp.h"

// Exception object
extern PyObject    *FieldMapCppError;
extern std::string  FieldMapCppMsg;


PyObject*  fieldmapcpp_interpolate_fieldmap(PyObject *self, PyObject *args) {

	PyObject *py_id, *py_pos;
	if (!PyArg_ParseTuple(args, "OO", &py_id, &py_pos))
		return NULL;

	size_t id = (size_t) PyLong_AsLong(py_id);

	Py_INCREF(py_pos);
	std::vector<double> pos;
	if (fieldmapcpp_read_pos(py_pos, pos)) {
		Py_DECREF(py_pos);
		return NULL;
	}
	Py_DECREF(py_pos);

	std::vector<Vector3D<double> > posv;
	for(size_t i=0; i<(pos.size()/3); ++i) {
		posv.push_back(Vector3D<double>(pos[3*i+0],pos[3*i+1],pos[3*i+2]));
	}
	std::vector<Vector3D<double> > field;
	interpolate_fieldmap(id, posv, field);
	//std::cout << pos.size() << std::endl;

	PyObject *py_lst  = PyList_New(3*field.size());
	for(size_t i=0; i<field.size(); ++i) {
		PyObject *py_bx = PyFloat_FromDouble(field[i].x);
		PyObject *py_by = PyFloat_FromDouble(field[i].y);
		PyObject *py_bz = PyFloat_FromDouble(field[i].z);
		PyList_SET_ITEM(py_lst, 3*i+0, py_bx);
		PyList_SET_ITEM(py_lst, 3*i+1, py_by);
		PyList_SET_ITEM(py_lst, 3*i+2, py_bz);
	}
	return py_lst;

}
