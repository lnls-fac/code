// TRACKC++
// ========
// Author: 		Ximenes R. Resende
// email:  		xresende@gmail.com, ximenes.resende@lnls.br
// affiliation:	LNLS - Laboratorio Nacional de Luz Sincrotron
// Date: 		Tue Dec 10 17:57:20 BRST 2013


#include "auxiliary.h"
#include "elements.h"
#include <cfloat>

const std::vector<double> Element::default_polynom = std::vector<double>(3,0);


// default constructor (constructs a drift element)
Element::Element(const std::string& fam_name_, const double& length_) :
    fam_name(fam_name_), length(length_) {
	for(unsigned int i=0; i<6; i++) {
		t_in[i] = t_out[i] = 0.0;
		for(unsigned int j=0; j<6; ++j) {
			if (i == j) {
				r_in[i*6+j] = r_out[i*6+j] = 1.0;
			} else {
				r_in[i*6+j] = r_out[i*6+j] = 0.0;
			}
		}
	}

};

Element Element::marker (const std::string& fam_name_) {
	Element e = Element(fam_name_, 0);
	e.pass_method = PassMethod::pm_identity_pass;
	return e;
}

Element Element::drift (const std::string& fam_name_, const double& length_) {
	Element e = Element(fam_name_, length_);
	e.pass_method = PassMethod::pm_drift_pass;
	return e;
}

Element Element::hcorrector(const std::string& fam_name_, const double& length_, const double& hkick_) {
	Element e = Element(fam_name_, length_);
	e.pass_method = PassMethod::pm_corrector_pass;
	e.hkick = hkick_;
	return e;
}

Element Element::vcorrector(const std::string& fam_name_, const double& length_, const double& vkick_) {
	Element e = Element(fam_name_, length_);
	e.pass_method = PassMethod::pm_corrector_pass;
	e.vkick = vkick_;
	return e;
}

Element Element::corrector(const std::string& fam_name_, const double& length_, const double& hkick_, const double& vkick_) {
	Element e = Element(fam_name_, length_);
	e.pass_method = PassMethod::pm_corrector_pass;
	e.hkick = hkick_;
	e.vkick = vkick_;
	return e;
}


Element Element::quadrupole (const std::string& fam_name_, const double& length_, const double& K_, const int nr_steps_) {
	Element e = Element(fam_name_, length_);
	e.pass_method = PassMethod::pm_str_mpole_symplectic4_pass;
	e.polynom_b[1] = K_;
	return e;
}

Element Element::sextupole (const std::string& fam_name_, const double& length_, const double& S_, const int nr_steps_) {
	Element e = Element(fam_name_, length_);
	e.nr_steps = nr_steps_;
	e.pass_method = PassMethod::pm_str_mpole_symplectic4_pass;
	e.polynom_b[2] = S_;
	return e;
}
Element Element::rbend (const std::string& fam_name_, const double& length_, const double& angle_, const double& angle_in_, const double& angle_out_, const double& K_, const double& S_) {
	Element e = Element(fam_name_, length_);
	e.pass_method = PassMethod::pm_bnd_mpole_symplectic4_pass;
	e.angle = angle_;
	e.angle_in = angle_in_;
	e.angle_out = angle_out_;
	e.polynom_b[1] = K_;
	e.polynom_b[2] = S_;
	return e;
}

Element Element::rfcavity (const std::string& fam_name_, const double& length_, const double& frequency_, const double& voltage_) {
	Element e = Element(fam_name_, length_);
	e.pass_method = PassMethod::pm_cavity_pass;
	e.frequency = frequency_;
	e.voltage = voltage_;
	return e;
}



void print_polynom(std::ostream& out, const std::string& label, const std::vector<double>& polynom) {
	int order = 0;
	for(unsigned int i=0; i<polynom.size(); ++i) {
		if (polynom[i] != 0) order = i+1;
	}
	if (order > 0) out << label;
	for(int i=0; i<order; ++i) {
		out << polynom[i] << " ";
	}
	if (order > 0) out << std::endl;
}

std::ostream& operator<< (std::ostream &out, const Element& el) {

	                      out << "fam_name      : " << el.fam_name << std::endl;
	if (el.length != 0)   out << "length        : " << el.length << std::endl;
	                      out << "pass_method   : " << pm_dict[el.pass_method] << std::endl;
	if (el.nr_steps > 1)  out << "nr_steps      : " << el.nr_steps << std::endl;
	if (el.thin_KL != 0)  out << "thin_KL       : " << el.thin_KL << std::endl;
	if (el.thin_SL != 0)  out << "thin_SL       : " << el.thin_SL << std::endl;
	if (el.angle != 0)    out << "bending_angle : " << el.angle << std::endl;
	if (el.angle != 0)    out << "entrance_angle: " << el.angle_in << std::endl;
	if (el.angle != 0)    out << "exit_angle    : " << el.angle_out << std::endl;
	if ((el.gap != 0) and ((el.fint_in != 0) or (el.fint_out != 0))) {
		                  out << "gap           : " << el.gap << std::endl;
		                  out << "fint_in       : " << el.fint_in << std::endl;
		                  out << "fint_out      : " << el.fint_out << std::endl;
	}
	print_polynom(        out,   "polynom_a     : ", el.polynom_a);
	print_polynom(        out,   "polynom_b     : ", el.polynom_b);
	if (el.frequency != 0)out << "frequency     : " << el.frequency << std::endl;
	if (el.voltage != 0)  out << "voltage       : " << el.voltage << std::endl;
	return out;
}



