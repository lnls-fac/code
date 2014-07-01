// TRACKC++
// ========
// Author: 		Ximenes R. Resende
// email:  		xresende@gmail.com, ximenes.resende@lnls.br
// affiliation:	LNLS - Laboratorio Nacional de Luz Sincrotron
// Date: 		Tue Dec 10 17:57:20 BRST 2013

#include "trackc++.h"
#include <ctime>

int test_printlattice(const std::vector<Element>& the_ring) {
	latt_print(the_ring);
	return 0;
}

int test_linepass(const Accelerator& accelerator, const std::vector<Element>& the_ring) {


	Pos<> pos;
	pos.rx = 1*0.00100; pos.px = 0*0.00001;
	pos.ry = 0*0.00010; pos.py = 0*0.00001;

	std::vector<Pos<> > new_pos;
	unsigned int element_offset = 0;
	Plane::type lost_plane;
	track_linepass(accelerator, pos, new_pos, element_offset, lost_plane, true);
	for(unsigned int i=0; i<new_pos.size(); ++i) {
		const Pos<>& c = new_pos[i];
		fprintf(stdout, "%03i: %15s  %+23.16E %+23.16E %+23.16E %+23.16E %+23.16E\n", i+1, the_ring[i % the_ring.size()].fam_name.c_str(), c.rx, c.px, c.ry, c.py, c.de);
	}


	return 0;

}

int test_linepass_tpsa(const Accelerator& accelerator, const std::vector<Element>& the_ring) {

	const int order = 3;
	Pos<Tpsa<6,order> > tpsa;

	tpsa.rx = Tpsa<6,order>(0, 0); tpsa.px = Tpsa<6,order>(0, 1);
	tpsa.ry = Tpsa<6,order>(0, 2); tpsa.py = Tpsa<6,order>(0, 3);
	tpsa.de = Tpsa<6,order>(0, 4); tpsa.dl = Tpsa<6,order>(0, 5);
	std::vector<Pos<Tpsa<6,order> > > new_tpsa;
	unsigned int element_offset = 0;
	Plane::type lost_plane;
	track_linepass(accelerator, tpsa, new_tpsa, element_offset, lost_plane, false);
	for(unsigned int i=0; i<new_tpsa.size(); ++i) {
		//const Pos<Tpsa<6,1> >& c = new_particles[i];
		//std::cout << c.rx << std::endl;
		//fprintf(stdout, "%03i: %15s  %+23.16E %+23.16E %+23.16E %+23.16E %+23.16E\n", i+1, the_ring[i].fam_name.c_str(), c.rx, c.px, c.ry, c.py, c.de);
	}

	return 0;

}

#include <cstdlib>
int test_ringpass(const Accelerator& accelerator, const std::vector<Element>& the_ring) {


	Pos<> pos;
	pos.rx = 0.00100;
	pos.ry = 0.00010;

	std::vector<Pos<double> > new_pos;
	unsigned int element_offset = 0, lost_turn = 0;
	Plane::type lost_plane;

	clock_t begin, end;
	double time_spent;
	begin = clock();
	Status::type status = track_ringpass(accelerator, pos, new_pos, 5000, lost_turn, element_offset, lost_plane, true);
	end = clock();
	time_spent = (double)(end - begin) / CLOCKS_PER_SEC;

	if (status != Status::success) {
		std::cerr << "problem" << std::endl;
	}
	for(unsigned int i=0; i<new_pos.size(); ++i) {
		const Pos<>& c = new_pos[i];
		fprintf(stdout, "%03i: %+23.16E %+23.16E %+23.16E %+23.16E %+23.16E\n", i+1, c.rx, c.px, c.ry, c.py, c.de);
	}
	std::cout << "tracking_time: " << time_spent << std::endl;

	return 0;

}

int test_findorbit6(const Accelerator& accelerator, const std::vector<Element>& the_ring) {

	std::vector<Pos<double> > orbit;
	Status::type status = track_findorbit6(accelerator, orbit);
	if (status == Status::findorbit_not_converged) {
		std::cerr << "findorbit not converged!" << std::endl;
	} else {
		const Pos<>& c = orbit[0];
		fprintf(stdout, "closed_orbit: %+23.16E %+23.16E %+23.16E %+23.16E %+23.16E\n", c.rx, c.px, c.ry, c.py, c.de);
	}
	return 0;
}

#include <cstdio>
int test_findm66(const Accelerator& accelerator, const std::vector<Element>& the_ring) {

	std::vector<double*> m66;

	std::vector<Pos<double> > cod;
	for(unsigned int i=0; i<the_ring.size(); ++i) {
		cod.push_back(Pos<double>());
		double *m = new double [36];
		m66.push_back(m);
	}

	track_findm66 (accelerator, cod, m66);

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

int test_dynap_xy(const Accelerator& accelerator) {

	std::vector<Pos<double> > closed_orbit;
	unsigned int nr_turns = 5000;
	Pos<double> p0(0,0,0,0,0,0);
	unsigned int nrpts_x = 10;
	double x_min = -0.015, x_max = +0.015;
	unsigned int nrpts_y = 10;
	double y_min = 0, y_max = +0.0035;
	std::vector<DynApGridPoint> points;
	dynap_xy(accelerator, closed_orbit, nr_turns, p0, nrpts_x, x_min, x_max, nrpts_y, y_min, y_max, true, points);

	return 0;
}

int test_cmd_dynap_xy() {

	char *argv[] = {
			(char*)"trackc++",
			(char*)"dynap_xy",
			(char*)"/home/fac_files/code/python/trackc++/tests/flat_file_v500_ac10_5_bare_in.txt",
			(char*)"3e9",
			(char*)"864",
			(char*)"on",
			(char*)"on",
			(char*)"on",
			(char*)"0.0",
			(char*)"5000",
			(char*)"2",
			(char*)"-0.015",
			(char*)"+0.015",
			(char*)"2",
			(char*)"0.0",
			(char*)"+0.0035",
			NULL};
	int argc = 0; while(argv[argc] != NULL) argc++;
	return cmd_dynap_xy(argc,argv);

}


int test_cmd_dynap_ex() {

	char *argv[] = {
			(char*)"trackc++",
			(char*)"dynap_ex",
			(char*)"/home/fac_files/code/python/trackc++/tests/flat_file_v500_ac10_5_bare_in.txt",
			(char*)"3e9",
			(char*)"864",
			(char*)"on",
			(char*)"on",
			(char*)"on",
			(char*)"1e-6",
			(char*)"5000",
			(char*)"2",
			(char*)"-0.05",
			(char*)"+0.05",
			(char*)"2",
			(char*)"-0.015",
			(char*)"+0.015",
			NULL};
	int argc = 0; while(argv[argc] != NULL) argc++;
	return cmd_dynap_xy(argc,argv);

}


int test_cmd_dynap_ma() {

	char *argv[] = {
			(char*)"trackc++",
			(char*)"dynap_ma",
			(char*)"/home/fac_files/code/python/trackc++/tests/flat_file_v500_ac10_5_bare_in.txt",
			(char*)"3e9",
			(char*)"864",
			(char*)"on",
			(char*)"on",
			(char*)"on",
			(char*)"5000",
			(char*)"30e-6",   // y0
			(char*)"0.01",    // e0
			(char*)"0.0001",  // tol_e
			(char*)"0",       // s_min [m]
			(char*)"30",      // s_max [m]
			(char*)"qaf",
			(char*)"qad",
			NULL};
	int argc = 0; while(argv[argc] != NULL) argc++;
	return cmd_dynap_ma(argc,argv);

}

int cmd_tests(int argc, char* argv[]) {


	//Accelerator accelerator
	//sirius_v500(accelerator.line);
	//accelerator.line = latt_read_flat_file("/home/ximenes/Desktop/flat_file_test.txt");
	//accelerator.harmonic_number = 864;


	//latt_setcavity(the_ring, "on");
	//latt_setradiation(the_ring, "on", 3e9);
	//the_ring[13].hkick = 1e-4;

	//std::vector<Element> the_ring2(the_ring);
	//the_ring2.insert(the_ring2.begin(), the_ring.begin(), the_ring.end());
	//latt_print(the_ring);
	//std::cout << the_ring.size() << std::endl;

	//test_printlattice(the_ring);
	//test_findm66(the_ring);
	//test_linepass(the_ring);
	//test_ringpass(the_ring);
	//test_linepass_tpsa(the_ring);
	//test_findorbit6(the_ring);
	//test_dynap_xy(the_ring);

	//test_cmd_dynap_xy();
	//test_cmd_dynap_ex();
	test_cmd_dynap_ma();
	return 0;

}
