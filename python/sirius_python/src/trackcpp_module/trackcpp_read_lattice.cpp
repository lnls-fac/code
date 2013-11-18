#include "trackcpp.h"

void read_polynom(PyObject *py_polynom, std::vector<double>& polynom) {
	polynom.clear();
	int nr_pts = PyList_Size(py_polynom);
	for(int i=0; i<nr_pts; ++i) {
		PyObject *py_item = PyList_GetItem(py_polynom, i);
		double value = PyFloat_AsDouble(py_item);
		polynom.push_back(value);
	}
}

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
		int pass_method = PassMethod::pm_identity_pass;
		if (PyObject_HasAttrString(py_element, "pass_method")) {
			PyObject *py_attr = PyObject_GetAttrString(py_element, "pass_method");
			if (py_attr != NULL) {
				pass_method = PyInt_AsLong(py_attr);
				Py_DECREF(py_attr);
			}
		}
		int nr_steps = 1;
		if (PyObject_HasAttrString(py_element, "nr_steps")) {
		PyObject *py_attr = PyObject_GetAttrString(py_element, "nr_steps");
			if (py_attr != NULL) {
				nr_steps = PyInt_AsLong(py_attr);
				Py_DECREF(py_attr);
			}
		}
		double thin_KL = 0.0;
		if (PyObject_HasAttrString(py_element, "kl")) {
			PyObject *py_attr = PyObject_GetAttrString(py_element, "kl");
			if (py_attr != NULL) {
				thin_KL = PyFloat_AsDouble(py_attr);
				Py_DECREF(py_attr);
			}
		}
		double thin_SL = 0.0;
		if (PyObject_HasAttrString(py_element, "sl")) {
			PyObject *py_attr = PyObject_GetAttrString(py_element, "sl");
			if (py_attr != NULL) {
				thin_SL = PyFloat_AsDouble(py_attr);
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
		std::vector<double> polynom_a;
		if (PyObject_HasAttrString(py_element, "polynom_a")) {
			PyObject *py_attr = PyObject_GetAttrString(py_element, "polynom_a");
			if (py_attr != NULL) {
				read_polynom(py_attr, polynom_a);
				Py_DECREF(py_attr);
			}
		}
		std::vector<double> polynom_b;
		if (PyObject_HasAttrString(py_element, "polynom_b")) {
			PyObject *py_attr = PyObject_GetAttrString(py_element, "polynom_b");
			if (py_attr != NULL) {
				read_polynom(py_attr, polynom_b);
				Py_DECREF(py_attr);
			}
		}
		std::vector<double> kick_angle = {0,0};
		if (PyObject_HasAttrString(py_element, "kick_angle")) {
			PyObject *py_attr = PyObject_GetAttrString(py_element, "kick_angle");
			if (py_attr != NULL) {
				read_polynom(py_attr, kick_angle);
				Py_DECREF(py_attr);
			}
		}; while(kick_angle.size() < 2) { kick_angle.push_back(0); };
		double angle_in = 0.0;
		if (PyObject_HasAttrString(py_element, "angle_in")) {
			PyObject *py_attr = PyObject_GetAttrString(py_element, "angle_in");
			if (py_attr != NULL) {
				angle_in = PyFloat_AsDouble(py_attr);
				Py_DECREF(py_attr);
			}
		}
		double angle_out = 0.0;
		if (PyObject_HasAttrString(py_element, "angle_out")) {
			PyObject *py_attr = PyObject_GetAttrString(py_element, "angle_out");
			if (py_attr != NULL) {
				angle_out = PyFloat_AsDouble(py_attr);
				Py_DECREF(py_attr);
			}
		}
		double gap = 0.0;
		if (PyObject_HasAttrString(py_element, "gap")) {
			PyObject *py_attr = PyObject_GetAttrString(py_element, "gap");
			if (py_attr != NULL) {
				gap = PyFloat_AsDouble(py_attr);
				Py_DECREF(py_attr);
			}
		}
		double fint1 = 0.0;
		if (PyObject_HasAttrString(py_element, "fint1")) {
			PyObject *py_attr = PyObject_GetAttrString(py_element, "fint1");
			if (py_attr != NULL) {
				fint1 = PyFloat_AsDouble(py_attr);
				Py_DECREF(py_attr);
			}
		}
		double fint2 = 0.0;
		if (PyObject_HasAttrString(py_element, "fint2")) {
			PyObject *py_attr = PyObject_GetAttrString(py_element, "fint2");
			if (py_attr != NULL) {
				fint1 = PyFloat_AsDouble(py_attr);
				Py_DECREF(py_attr);
			}
		}
		double frequency = 0.0;
		if (PyObject_HasAttrString(py_element, "frequency")) {
			PyObject *py_attr = PyObject_GetAttrString(py_element, "frequency");
			if (py_attr != NULL) {
				frequency = PyFloat_AsDouble(py_attr);
				Py_DECREF(py_attr);
			}
		}
		double voltage = 0.0;
		if (PyObject_HasAttrString(py_element, "voltage")) {
			PyObject *py_attr = PyObject_GetAttrString(py_element, "voltage");
			if (py_attr != NULL) {
				voltage = PyFloat_AsDouble(py_attr);
				Py_DECREF(py_attr);
			}
		}
		double energy = 0.0;
		if (PyObject_HasAttrString(py_element, "energy")) {
			PyObject *py_attr = PyObject_GetAttrString(py_element, "energy");
			if (py_attr != NULL) {
				energy = PyFloat_AsDouble(py_attr);
				Py_DECREF(py_attr);
			}
		}


//		double				thin_KL, thin_SL;
//		double              err_dx, err_dy, err_excit;
//		double              err_roll, err_yaw, err_pitch;


		while (polynom_a.size() < polynom_b.size()) polynom_a.push_back(0);
		while (polynom_b.size() < polynom_a.size()) polynom_b.push_back(0);

		Element el = Element(fam_name, length);
		el.pass_method = pass_method;
		el.angle       = angle;
		el.nr_steps    = nr_steps;
		el.polynom_a   = polynom_a;
		el.polynom_b   = polynom_b;
		el.angle_in    = angle_in;
		el.angle_out   = angle_out;
		el.gap         = gap;
		el.fint1       = fint1;
		el.fint2       = fint2;
		el.thin_KL     = thin_KL;
		el.thin_SL     = thin_SL;
		el.frequency   = frequency;
		el.voltage     = voltage;
		el.energy      = energy;
		el.hkick       = kick_angle[0];
		el.vkick       = kick_angle[1];

		v.push_back(el);
		std::cout << "Element#     : " << i+1 << std::endl;
		std::cout << el << std::endl;

	}
}
