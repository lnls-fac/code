#ifndef _ELEMENT_H
#define _ELEMENT_H

// TRACKC++
// ========
// Author: 		Ximenes R. Resende
// email:  		xresende@gmail.com, ximenes.resende@lnls.br
// affiliation:		LNLS - Laboratorio Nacional de Luz Sincrotron
// Date: 		Tue Dec 10 17:57:20 BRST 2013

#include "kicktable.h"
#include "auxiliary.h"
#include <vector>
#include <string>
#include <fstream>
#include <cfloat>

class Element {
public:

//	fam_name(fam_name_), pass_method(PassMethod::pm_drift_pass),
//		nr_steps(1), length(length_),
//		hkick(0), vkick(0),
//		angle(0), angle_in(0), angle_out(0),
//		gap(0), fint_in(0), fint_out(0),
//		thin_KL(0), thin_SL(0),
//		frequency(0), voltage(0),
//		polynom_a(default_polynom), polynom_b(default_polynom),
//		hmax(DBL_MAX), vmax(DBL_MAX)

	std::string			fam_name;
	int					pass_method = PassMethod::pm_drift_pass;
	double				length      = 0;
	int					nr_steps    = 1;
	double				hkick       = 0;
	double				vkick       = 0;
	double				angle       = 0;
	double				angle_in    = 0;
	double				angle_out   = 0;
	double				gap         = 0;
	double              fint_in     = 0;
	double              fint_out    = 0;
	double				thin_KL     = 0;
	double				thin_SL     = 0;
	double              frequency   = 0;
	double              voltage     = 0;
	std::vector<double> polynom_a   = default_polynom;
	std::vector<double> polynom_b   = default_polynom;
	const Kicktable*    kicktable   = nullptr;
	double              hmax        = DBL_MAX;
	double              vmax        = DBL_MAX;
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
