#include "trackc++.h"

// Exception object
extern PyObject *TrackcppError;
extern std::string TrackcppErrorMsg;


void read_vector(PyObject *py_polynom, std::vector<double>& polynom) {
	polynom.clear();
	int nr_pts = PyList_Size(py_polynom);
	for(int i=0; i<nr_pts; ++i) {
		PyObject *py_item = PyList_GetItem(py_polynom, i);
		double value = PyFloat_AsDouble(py_item);
		polynom.push_back(value);
	}
}

int trackcpp_read_lattice(PyObject *py_lattice, std::vector<Element>& v) {

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
				read_vector(py_attr, polynom_a);
				Py_DECREF(py_attr);
			}
		}
		std::vector<double> polynom_b;
		if (PyObject_HasAttrString(py_element, "polynom_b")) {
			PyObject *py_attr = PyObject_GetAttrString(py_element, "polynom_b");
			if (py_attr != NULL) {
				read_vector(py_attr, polynom_b);
				Py_DECREF(py_attr);
			}
		}

		std::vector<double> kick_angle; kick_angle.push_back(0); kick_angle.push_back(0);
		if (PyObject_HasAttrString(py_element, "kick_angle")) {
			PyObject *py_attr = PyObject_GetAttrString(py_element, "kick_angle");
			if (py_attr != NULL) {
				read_vector(py_attr, kick_angle);
				Py_DECREF(py_attr);
			}
		}; while(kick_angle.size() < 2) { kick_angle.push_back(0); };
		//std::cout << "kickangle: " << kick_angle[0] << kick_angle[1] << std::endl;

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
		double fint_in = 0.0;
		if (PyObject_HasAttrString(py_element, "fint_in")) {
			PyObject *py_attr = PyObject_GetAttrString(py_element, "fint_in");
			if (py_attr != NULL) {
				fint_in = PyFloat_AsDouble(py_attr);
				Py_DECREF(py_attr);
			}
		}
		double fint_out = 0.0;
		if (PyObject_HasAttrString(py_element, "fint_out")) {
			PyObject *py_attr = PyObject_GetAttrString(py_element, "fint_out");
			if (py_attr != NULL) {
				fint_out = PyFloat_AsDouble(py_attr);
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
		std::vector<double> t_in;
		if (PyObject_HasAttrString(py_element, "t_in")) {
			PyObject *py_attr = PyObject_GetAttrString(py_element, "t_in");
			if (py_attr != NULL) {
				read_vector(py_attr, t_in);
				Py_DECREF(py_attr);
			}
		}
		std::vector<double> t_out;
		if (PyObject_HasAttrString(py_element, "t_out")) {
			PyObject *py_attr = PyObject_GetAttrString(py_element, "t_out");
			if (py_attr != NULL) {
				read_vector(py_attr, t_out);
				Py_DECREF(py_attr);
			}
		}
		std::vector<double> r_in;
		if (PyObject_HasAttrString(py_element, "r_in")) {
			PyObject *py_attr = PyObject_GetAttrString(py_element, "r_in");
			if (py_attr != NULL) {
				read_vector(py_attr, r_in);
				Py_DECREF(py_attr);
			}
		}
		std::vector<double> r_out;
		if (PyObject_HasAttrString(py_element, "r_out")) {
			PyObject *py_attr = PyObject_GetAttrString(py_element, "r_out");
			if (py_attr != NULL) {
				read_vector(py_attr, r_out);
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
		el.fint_in     = fint_in;
		el.fint_out    = fint_out;
		el.thin_KL     = thin_KL;
		el.thin_SL     = thin_SL;
		el.frequency   = frequency;
		el.voltage     = voltage;
		el.hkick       = kick_angle[0];
		el.vkick       = kick_angle[1];

		// inserts translation vector and rotation matrix
		if ((t_in.size()  !=  0) and (t_in.size()  != 6)) {
			std::ostringstream convert; convert << i; std::string strnumber = convert.str();
			TrackcppErrorMsg = "Incorrect parameters in 't_in' for element #" +  strnumber;
			//TrackcppErrorMsg = "Incorrect parameters in 't_in' for element #" + std::to_string(i);
			PyErr_SetString(TrackcppError, TrackcppErrorMsg.c_str());
			return -1;
		} else {
			for(unsigned int j=0;j<t_in.size();++j) el.t_in[j] = t_in[j];
		}
		if ((t_out.size()  !=  0) and (t_out.size()  != 6)) {
			std::ostringstream convert; convert << i; std::string strnumber = convert.str();
			TrackcppErrorMsg = "Incorrect parameters in 't_out' for element #" +  strnumber;
			//TrackcppErrorMsg = "Incorrect parameters in 't_out' for element #" + std::to_string(i);
			PyErr_SetString(TrackcppError, TrackcppErrorMsg.c_str());
			return -1;
		} else {
			for(unsigned int j=0;j<t_out.size();++j) el.t_out[j] = t_out[j];
		}
		if ((r_in.size()  !=  0) and (r_in.size()  != 36)) {
			std::ostringstream convert; convert << i; std::string strnumber = convert.str();
			TrackcppErrorMsg = "Incorrect parameters in 'r_in' for element #" +  strnumber;
			//TrackcppErrorMsg = "Incorrect parameters in 'r_in' for element #" + std::to_string(i);
			PyErr_SetString(TrackcppError, TrackcppErrorMsg.c_str());
			return -1;
		} else {
			for(unsigned int j=0;j<r_in.size();++j) el.r_in[j] = r_in[j];
		}
		if ((r_out.size()  !=  0) and (r_out.size()  != 36)) {
			std::ostringstream convert; convert << i; std::string strnumber = convert.str();
			TrackcppErrorMsg = "Incorrect parameters in 'r_out' for element #" +  strnumber;
			//TrackcppErrorMsg = "Incorrect parameters in 'r_out' for element #" + std::to_string(i);
			PyErr_SetString(TrackcppError, TrackcppErrorMsg.c_str());
			return -1;
		} else {
			for(unsigned int j=0;j<r_out.size();++j) el.r_out[j] = r_out[j];
		}


		v.push_back(el);

		//std::cout << "Element#     : " << i+1 << std::endl;
		//std::cout << el << std::endl;

	}

	return 0;

}
