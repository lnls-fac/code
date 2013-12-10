// TRACKC++
// ========
// Author: 		Ximenes R. Resende
// email:  		xresende@gmail.com, ximenes.resende@lnls.br
// affiliation:	LNLS - Laboratorio Nacional de Luz Sincrotron
// Date: 		Tue Dec 10 17:57:20 BRST 2013


#include "auxiliary.h"
#include "elements.h"

const std::vector<double> Element::default_polynom = std::vector<double>(3,0);


// default constructor (constructs a drift element)
Element::Element(const std::string& fam_name_, const double& length_) :
	fam_name(fam_name_), pass_method(PassMethod::pm_drift_pass),
	nr_steps(1), length(length_),
	hkick(0), vkick(0),
	angle(0), angle_in(0), angle_out(0),
	gap(0), fint_in(0), fint_out(0),
	thin_KL(0), thin_SL(0),
	frequency(0), voltage(0), energy(0),
	//err_dx(0), err_dy(0), err_excit(0),
	//err_roll(0), err_yaw(0), err_pitch(0),
	polynom_a(default_polynom), polynom_b(default_polynom)
{
	//polynom_a.clear();
	//polynom_b.clear();
	//t1.set_zero(); t2.set_zero();
	//r1.set_identity(); r2.set_identity();
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

Element Element::drift (const std::string& fam_name_, const double& length_) {
	Element e = Element(fam_name_, length_);
	e.pass_method = PassMethod::pm_drift_pass;
	return e;
}


Element Element::quadrupole (const std::string& fam_name_, const double& length_, const double& K_) {
	Element e = Element(fam_name_, length_);
	e.pass_method = PassMethod::pm_str_mpole_symplectic4_pass;
	e.polynom_b[1] = K_;
	return e;
}

Element Element::sextupole (const std::string& fam_name_, const double& length_, const double& S_) {
	Element e = Element(fam_name_, length_);
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

Element Element::rfcavity (const std::string& fam_name_, const double& length_, const double& frequency_, const double& voltage_, const double& energy_) {
	Element e = Element(fam_name_, length_);
	e.pass_method = PassMethod::pm_cavity_pass;
	e.frequency = frequency_;
	e.voltage = voltage_;
	e.energy = energy_;
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

std::ostream& operator<< (std::ostream &out, Element& el) {

	out << "FamName      : " << el.fam_name << std::endl;
	if (el.length != 0) out << "Length       : " << el.length << std::endl;
	out << "PassMethod   : " << passmethods[el.pass_method] << std::endl;
	if (el.nr_steps > 1) out << "NrSteps      : " << el.nr_steps << std::endl;
	if (el.thin_KL != 0)  out << "ThinKL       : " << el.thin_KL << std::endl;
	if (el.thin_SL != 0)  out << "ThinSL       : " << el.thin_SL << std::endl;
	if (el.angle != 0)  out << "BendingAngle : " << el.angle << std::endl;
	if (el.angle != 0)  out << "EntranceAngle: " << el.angle_in << std::endl;
	if (el.angle != 0)  out << "ExitAngle    : " << el.angle_out << std::endl;
	if ((el.gap != 0) and ((el.fint_in != 0) or (el.fint_out != 0))) {
		out << "Gap          : " << el.gap << std::endl;
		out << "FInt1        : " << el.fint_in << std::endl;
		out << "FInt2        : " << el.fint_out << std::endl;
	}
	print_polynom(out, "PolynomA     : ", el.polynom_a);
	print_polynom(out, "PolynomB     : ", el.polynom_b);
	if (el.frequency != 0) out << "Frequency    : " << el.frequency << std::endl;
	if (el.voltage != 0)   out << "Voltage      : " << el.voltage << std::endl;
	if (el.energy != 0)    out << "Frequency    : " << el.energy << std::endl;
	return out;
}



