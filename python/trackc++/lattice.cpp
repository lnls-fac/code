#include "auxiliary.h"
#include "elements.h"

void printlattice(std::vector<Element>& lattice) {

	for(unsigned int i=0; i<lattice.size(); ++i) {
		std::cout << "element#     : " << i+1 << std::endl;
		std::cout << lattice[i];
		std::cout << std::endl;
	}
}
