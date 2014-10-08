// TRACKC++
// ========
// Author: 		Ximenes R. Resende
// email:  		xresende@gmail.com, ximenes.resende@lnls.br
// affiliation:		LNLS - Laboratorio Nacional de Luz Sincrotron
// Date: 		Tue Dec 10 17:57:20 BRST 2013

#include "passmethods.h"
#include "auxiliary.h"


double get_magnetic_rigidity(const double energy) {
    double gamma = (energy/1e6) / (electron_rest_energy_MeV);
    double beta  = sqrt(1 - 1/(gamma*gamma));
    double b_rho = beta * energy / light_speed; // [T.m]
    return b_rho;
}
