#ifndef _ELEMENT_H
#define _ELEMENT_H

#include "trackc++.h"

class Element {
public:

	std::string			fam_name;
	int					pass_method;
	int					nr_steps;
	double				length;
	double				hkick, vkick;
	double				angle, angle_in, angle_out;
	double				gap, fint1, fint2;
	double				thin_KL, thin_SL;
	double              err_dx, err_dy, err_excit;
	double              err_roll, err_yaw, err_pitch;
	std::vector<double> polynom_a, polynom_b;

	// default constructor (builds a drift-type element)
	Element(const std::string& fam_name_ = "", const double& length_ = 0);

	static const std::vector<double> default_polynom;

	// front-end routines for typed element creation
	static Element marker     (const std::string& fam_name_);
	static Element bpm        (const std::string& fam_name_);
	static Element hcorrector (const std::string& fam_name_, const double& length_, const double& kick_);
	static Element vcorrector (const std::string& fam_name_, const double& length_, const double& kick_);
	static Element drift      (const std::string& fam_name_, const double& length_);
	static Element rbend      (const std::string& fam_name_, const double& length_, const double& angle_, const double& angle_in_ = 0, const double& angle_out_ = 0, const double& K_ = 0, const double& S_ = 0);
	static Element quadrupole (const std::string& fam_name_, const double& length_, const double& K_);
	static Element sextupole  (const std::string& fam_name_, const double& length_, const double& S_);

	friend std::ostream& operator<< (std::ostream &out, Element& el);

};

#endif
