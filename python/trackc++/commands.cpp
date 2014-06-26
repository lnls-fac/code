#include "commands.h"
#include "dynap.h"
#include "flat_file.h"
#include "lattice.h"
#include "elements.h"
#include "auxiliary.h"
#include <string>
#include <cstdlib>
#include <iostream>

int cmd_dynap_xy(int argc, char* argv[]) {

	if (argc != 8) {
		std::cerr << "dynap_xy: invalid number of arguments!" << std::endl;
		return EXIT_FAILURE;
	}

	std::string flat_filename(argv[2]);
	double      ring_energy      = std::atof(argv[3]);
	unsigned int harmonic_number = std::atoi(argv[4]);
	std::string cavity_state(argv[5]);
	std::string radiation_state(argv[6]);
	unsigned int nr_turns = std::atoi(argv[7]);
	unsigned int nrpts_x = 10;
	double x_min = -0.010;
	double x_max = 0.010;
	unsigned int nrpts_y = 10;
	double y_min = 0;
	double y_max = 0.0035;

	std::cout << "<dynap_xy>" << std::endl;
	std::cout << "flat_filename: " << flat_filename << std::endl;
	std::cout << "energy: " << ring_energy << " [eV]" << std::endl;
	std::cout << "harmonic_number: " << harmonic_number << std::endl;
	std::cout << "cavity_state: " << cavity_state << std::endl;
	std::cout << "radiation_state: " << radiation_state << std::endl;
	std::cout << "nr_turns: " << nr_turns << std::endl;

	// reads flat file
	std::vector<Element> the_ring;
	Status::type status = read_flat_file_tracy(flat_filename, the_ring);
	if (status == Status::file_not_found) {
		std::cerr << "dynap_xy: flat file not found!" << std::endl;
		return EXIT_FAILURE;
	}

	// sets cavity and radiation state
	latt_setcavity(the_ring, cavity_state);
	latt_setradiation(the_ring, radiation_state, ring_energy);

	// calcs dynamical aperture
	std::vector<Pos<double> > cod;
	Pos<double> p0(0,0,0,0,0,0);
	std::vector<DynApPoint> points;
	dynap_xy(the_ring, harmonic_number, cod, nr_turns, p0, nrpts_x, x_min, x_max, nrpts_y, y_min, y_max, true, points);

	// generates output files
	return EXIT_SUCCESS;

}
