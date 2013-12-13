// TRACKC++
// ========
// Author: 		Ximenes R. Resende
// email:  		xresende@gmail.com, ximenes.resende@lnls.br
// affiliation:	LNLS - Laboratorio Nacional de Luz Sincrotron
// Date: 		Tue Dec 10 17:57:20 BRST 2013


#include "auxiliary.h"
#include "elements.h"

void printlattice(std::vector<Element>& lattice) {

	for(unsigned int i=0; i<lattice.size(); ++i) {
		std::cout << "element#     : " << i+1 << std::endl;
		std::cout << lattice[i];
		std::cout << std::endl;
	}
}
