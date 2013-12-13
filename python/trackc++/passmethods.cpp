// TRACKC++
// ========
// Author: 		Ximenes R. Resende
// email:  		xresende@gmail.com, ximenes.resende@lnls.br
// affiliation:	LNLS - Laboratorio Nacional de Luz Sincrotron
// Date: 		Tue Dec 10 17:57:20 BRST 2013


#include "auxiliary.h"
#include "passmethods.h"

std::string passmethods[] = {
		std::string("pm_identity_pass"),
		std::string("pm_drift_pass"),
		std::string("pm_str_mpole_symplectic_pass"),
		std::string("pm_bnd_mpole_symplectic_pass"),
		std::string("pm_corrector_pass"),
		std::string("pm_cavity_pass"),
		std::string("pm_thinquad_pass"),
		std::string("pm_thinsext_pass")
};
