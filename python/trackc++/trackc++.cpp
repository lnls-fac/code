// TRACKC++
// ========
// Author: 		Ximenes R. Resende
// email:  		xresende@gmail.com, ximenes.resende@lnls.br
// affiliation:	LNLS - Laboratorio Nacional de Luz Sincrotron
// Date: 		Tue Dec 10 17:57:20 BRST 2013


#include "trackc++.h"

int main() {

	//return 0;

	Element ds = Element::drift("ds", 1.1);
	Element qd = Element::quadrupole("qd", 1.2, 3.0);
	Element sf = Element::sextupole("sf", 1.2, -3.2);
	Element di = Element::rbend("di", 1.1, 0.1234, 0, 0, 0.1, 4.1);

	std::vector<Element> the_ring;

	the_ring.push_back(ds);
	the_ring.push_back(qd);
	the_ring.push_back(sf);
	the_ring.push_back(di);

	printlattice(the_ring);

	std::vector<Pos<> > particles;
	Pos<> pos;
	pos.rx = 0.001;
	particles.push_back(pos);

	Status::type stat;
	int element_idx;
	std::vector<Pos<> > new_particles;
	if ((stat = linepass (the_ring, particles, new_particles, &element_idx, false)) != Status::success) {
		std::cerr << "Error: " << stat << std::endl;
	}

	return 0;
}
