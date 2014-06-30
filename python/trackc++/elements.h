#ifndef _ELEMENT_H
#define _ELEMENT_H

// TRACKC++
// ========
// Author: 		Ximenes R. Resende
// email:  		xresende@gmail.com, ximenes.resende@lnls.br
// affiliation:		LNLS - Laboratorio Nacional de Luz Sincrotron
// Date: 		Tue Dec 10 17:57:20 BRST 2013

#include "auxiliary.h"


class Element {
public:

	std::string			fam_name;
	int					pass_method;
	int					nr_steps;
	double				length;
	double				hkick, vkick;
	double				angle, angle_in, angle_out;
	double				gap, fint_in, fint_out;
	double				thin_KL, thin_SL;
	double              frequency, voltage;
	std::vector<double> polynom_a, polynom_b;
	double              hmax, vmax;
	double				t_in[6],  t_out[6];
	double				r_in[36], r_out[36];


	// default constructor (builds a drift-type element)
	Element(const std::string& fam_name_ = "", const double& length_ = 0);

	static const std::vector<double> default_polynom;

	// front-end routines for typed element creation
	static Element marker     (const std::string& fam_name_);
	static Element bpm        (const std::string& fam_name_);
	static Element hcorrector (const std::string& fam_name_, const double& length_, const double& hkick_);
	static Element vcorrector (const std::string& fam_name_, const double& length_, const double& vkick_);
	static Element corrector  (const std::string& fam_name_, const double& length_, const double& hkick_, const double& vkick_);
	static Element drift      (const std::string& fam_name_, const double& length_);
	static Element rbend      (const std::string& fam_name_, const double& length_, const double& angle_, const double& angle_in_ = 0, const double& angle_out_ = 0, const double& K_ = 0, const double& S_ = 0);
	static Element quadrupole (const std::string& fam_name_, const double& length_, const double& K_, const int nt_steps_ = 1);
	static Element sextupole  (const std::string& fam_name_, const double& length_, const double& S_, const int nr_steps_ = 1);
	static Element rfcavity   (const std::string& fam_name_, const double& length_, const double& frequency_, const double& voltage_);

	friend std::ostream& operator<< (std::ostream &out, const Element& el);

};

#endif
