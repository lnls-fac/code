// TRACKC++
// ========
// Author: 		Ximenes R. Resende
// email:  		xresende@gmail.com, ximenes.resende@lnls.br
// affiliation:	LNLS - Laboratorio Nacional de Luz Sincrotron
// Date: 		Tue Dec 10 17:57:20 BRST 2013


#include "trackc++.h"

int create_model(std::vector<Element>& the_ring) {

	//return 0;

	Element ds = Element::drift      ("ds", 1.1);
	Element qd = Element::quadrupole ("qd", 1.2, 3.0);
	Element sf = Element::sextupole  ("sf", 1.2, -3.2);
	Element di = Element::rbend      ("di", 1.1, 0.1234, 0, 0, 0.1, 4.1);

	//std::vector<Element> the_ring;
	//the_ring.clear();

	the_ring.push_back(ds);
	the_ring.push_back(qd);
	the_ring.push_back(sf);
	the_ring.push_back(di);

//	printlattice(the_ring);
//
//	std::vector<Pos<> > particles;
//	Pos<> pos;
//	pos.rx = 0.001;
//	particles.push_back(pos);
//
//	Status::type stat;
//	int element_idx;
//	std::vector<Pos<> > new_particles;
//	if ((stat = linepass (the_ring, particles, new_particles, &element_idx, false)) != Status::success) {
//		std::cerr << "Error: " << stat << std::endl;
//	}

	return 0;
}

#include <cstdio>

int test_findm66() {

	std::vector<Element> the_ring;

	create_model(the_ring);

	std::vector<double*> m66;

	std::vector<Pos<double> > cod;
	for(unsigned int i=0; i<the_ring.size(); ++i) {
		cod.push_back(Pos<double>());
		double *m = new double [36];
		m66.push_back(m);
	}

	findm66 (the_ring, cod, m66);

	for(unsigned int i=0; i<the_ring.size(); ++i) {
		std::cout << "element#     : " << i+1 << std::endl;
		std::cout << the_ring[i];
		for(unsigned int r=0; r<6; ++r) {
			for(unsigned int c=0; c<6; ++c) {
				printf("%+10.4E ", (m66[i])[6*r+c]);
			}
			std::cout << std::endl;
		}
		std::cout << std::endl;
	}

	return 0;

}

int main() {

	test_findm66();

}
