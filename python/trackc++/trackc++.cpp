// TRACKC++
// ========
// Author: 		Ximenes R. Resende
// email:  		xresende@gmail.com, ximenes.resende@lnls.br
// affiliation:	LNLS - Laboratorio Nacional de Luz Sincrotron
// Date: 		Tue Dec 10 17:57:20 BRST 2013

#include "trackc++.h"

int test_linepass(const std::vector<Element>& the_ring) {


	std::vector<Pos<> > particles;
	Pos<> pos;
	pos.rx = 0.00100; pos.px = 0.00001;
	pos.ry = 0.00010; pos.py = 0.00001;
	particles.push_back(pos);

	std::vector<Pos<> > new_particles;
	int element_offset = 0;
	linepass(the_ring, particles, new_particles, &element_offset, true);
	for(unsigned int i=0; i<new_particles.size(); ++i) {
		const Pos<>& c = new_particles[i];
		fprintf(stdout, "%03i: %15s  %+23.16E %+23.16E %+23.16E %+23.16E %+23.16E\n", i+1, the_ring[i % the_ring.size()].fam_name.c_str(), c.rx, c.px, c.ry, c.py, c.de);
	}


	return 0;

}

int test_linepass_tpsa(const std::vector<Element>& the_ring) {

	const int order = 7;
	std::vector<Pos<Tpsa<6,order> > > particles;
	particles.push_back(Tpsa<6,order>());
	particles[0].rx = Tpsa<6,order>(0, 0); particles[0].px = Tpsa<6,order>(0, 1);
	particles[0].ry = Tpsa<6,order>(0, 2); particles[0].py = Tpsa<6,order>(0, 3);
	particles[0].de = Tpsa<6,order>(0, 4); particles[0].dl = Tpsa<6,order>(0, 5);
	std::vector<Pos<Tpsa<6,order> > > new_particles;
	int element_offset = 0;
	linepass(the_ring, particles, new_particles, &element_offset, false);
	for(unsigned int i=0; i<new_particles.size(); ++i) {
		//const Pos<Tpsa<6,1> >& c = new_particles[i];
		//std::cout << c.rx << std::endl;
		//fprintf(stdout, "%03i: %15s  %+23.16E %+23.16E %+23.16E %+23.16E %+23.16E\n", i+1, the_ring[i].fam_name.c_str(), c.rx, c.px, c.ry, c.py, c.de);
	}

	return 0;

}

#include <cstdlib>
int test_ringpass(const std::vector<Element>& the_ring) {


	std::vector<Pos<> > particles;
	Pos<> pos;
	pos.rx = 0.00100;
	pos.ry = 0.00010;
	particles.push_back(pos);

	std::vector<Pos<> > new_particles;
	int element_offset = 0, turn_idx = 0;

	ringpass(the_ring, particles, new_particles, 5000, &turn_idx, &element_offset);

	for(unsigned int i=0; i<new_particles.size(); ++i) {
		const Pos<>& c = new_particles[i];
		//fprintf(stdout, "%03i: %+20.17E %+20.17E %+20.17E %+20.17E %+20.17E\n", i+1, c.rx, c.px, c.ry, c.py, c.de);
		fprintf(stdout, "%03i: %+23.16E %+23.16E %+23.16E %+23.16E %+23.16E\n", i+1, c.rx, c.px, c.ry, c.py, c.de);
	}

	return 0;

}
#include <cstdio>

int test_findm66(const std::vector<Element>& the_ring) {

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


	std::vector<Element> the_ring;

	sirius_v500(the_ring);
	//the_ring = latt_read_flat_file("/home/ximenes/Desktop/flat_file_test.txt");

	latt_setcavity(the_ring, "on");
	latt_setradiation(the_ring, "on", 3e9);

	//std::vector<Element> the_ring2(the_ring);
	//the_ring2.insert(the_ring2.begin(), the_ring.begin(), the_ring.end());
	//latt_print(the_ring);
	//std::cout << the_ring.size() << std::endl;

	//test_findm66(the_ring);
	test_linepass(the_ring);
	//test_ringpass(the_ring);
	//test_linepass_tpsa(the_ring);

}
