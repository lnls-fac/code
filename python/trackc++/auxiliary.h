#ifndef _AUXILIARY_H
#define _AUXILIARY_H

// TRACKC++
// ========
// Author: 		Ximenes R. Resende
// email:  		xresende@gmail.com, ximenes.resende@lnls.br
// affiliation:	LNLS - Laboratorio Nacional de Luz Sincrotron
// Date: 		Tue Dec 10 17:57:20 BRST 2013

#include <vector>
#include <string>
#include <ostream>
#include <iostream>
#include <cmath>

// Important: 	the order of these passmethods and the order
// ==========	of the pyring passmethods have to be the same
//				so that python can correctly call trackcpp
//				module.

struct PassMethod {
	enum type {
		pm_identity_pass                  = 0,
		pm_drift_pass                     = 1,
		pm_str_mpole_symplectic4_pass     = 2,
		pm_bnd_mpole_symplectic4_pass     = 3,
		pm_corrector_pass                 = 4,
		pm_cavity_pass                    = 5,
		pm_thinquad_pass                  = 6,
		pm_thinsext_pass                  = 7,
		pm_str_mpole_symplectic4_rad_pass = 8,
		pm_bnd_mpole_symplectic4_rad_pass = 9
	};
};

const std::string pm_dict[] = {
		"identity_pass",
		"drift_pass",
		"str_mpole_symplectic4_pass",
		"bnd_mpole_symplectic4_pass",
		"corrector_pass",
		"cavity_pass",
		"thinquad_pass",
		"thinsext_pass",
		"str_mpole_symplectic4_rad_pass",
		"bnd_mpole_symplectic4_rad_pass"
};

struct Status {
	enum type {
		success = 0,
		passmethod_not_defined = 1,
		passmethod_not_implemented = 2,
		particle_lost = 3,
		inconsistent_dimensions = 4,
		uninitialized_memory = 5
	};
};

extern std::string passmethods[];

template <typename T> class Pos;
class Element;

const double light_speed          = 299792458;         // [m/s]   - definition
const double vacuum_permeability  = 4*M_PI*1e-7;       // [T.m/A] - definition
const double electron_charge      = 1.60217656535e-19; // [C]     - 2014-06-11
const double electron_mass        = 9.1093829140e-31;  // [Kg]    - 2014-06-11
const double electron_rest_energy = electron_mass * pow(light_speed,2);           // [Kg.m^2/s^2] - derived
const double vaccum_permitticity  = 1/(vacuum_permeability * pow(light_speed,2)); // [V.s/(A.m)]  - derived
const double electron_radius      = pow(electron_charge,2)/(4*M_PI*vaccum_permitticity*electron_rest_energy); // [m] - derived


typedef double Vector4[4];
typedef double Vector6[6];
typedef double Matrix4[4][4];
typedef double Matrix6[6][6];

#undef sqr

#endif
