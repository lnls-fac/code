#include "trackc++.h"
#include "output.h"
#include "dynap.h"
#include "tracking.h"
#include "lattice.h"
#include "pos.h"
#include "auxiliary.h"
#include <vector>
#include <cfloat>

static const double tiny_amp = 1e-6; // [m]

Status::type dynap_xy(
		const Accelerator& accelerator,
		std::vector<Pos<double> >& cod,
		unsigned int nr_turns,
		const Pos<double>& p0,
		unsigned int nrpts_x, double x_min, double x_max,
		unsigned int nrpts_y, double y_min, double y_max,
		bool calculate_closed_orbit,
		std::vector<DynApGridPoint>& grid
	) {

	const std::vector<Element>& the_ring = accelerator.lattice;

	// finds 6D closed-orbit
	if (calculate_closed_orbit) {
		if (verbose_on) {
			std::cout << get_timestamp() << " <" << __FUNCTION__ << ">: calculating closed-orbit...";
			std::cout.flush();
		}
		Status::type status = track_findorbit6(accelerator, cod);
		if (status != Status::success) return status;
		if (verbose_on) {
			std::cout << "ok" << std::endl;
		}
	}

	char buffer[1024];

	// main loop
	if (verbose_on) std::cout << get_timestamp() << " looping over dynap_xy points" << std::endl;
	grid.resize(nrpts_x * nrpts_y);
	int idx = 0;
	for(unsigned int i=0; i<nrpts_x; ++i) {
		double x = x_min + i * (x_max - x_min) / (nrpts_x - 1.0);
		if (fabs(x) < tiny_amp) x = sgn(x) * tiny_amp;
		for(unsigned int j=0; j<nrpts_y; ++j) {
			double y = y_min + j * (y_max - y_min) / (nrpts_y - 1.0);
			if (fabs(y) < tiny_amp) y = sgn(y) * tiny_amp;
			// prepares initial position
			Pos<double> p = p0;     // offset
			p.rx += x; p.ry += y;   // dynapt around closed-orbit
			grid[idx].p = p;        // registers initial condition
			p += cod[0];			// adds closed-orbit
			std::vector<Pos<double> > new_pos;
			int lost_turn = 0, lost_element = 0;
			if (verbose_on) {
				sprintf(buffer, "(%03i,%03i): x=%+11.4E [m], y=%+11.4E [m] -> ", i+1, j+1, x, y);
				std::cout << buffer; std::cout.flush();
			}
			Status::type status = track_ringpass (accelerator, the_ring, p, new_pos, nr_turns, lost_turn, lost_element, false);
			grid[idx].lost_turn = lost_turn;
			grid[idx].lost_element = lost_element;
			if (verbose_on) {
				sprintf(buffer, "turn=%05i element=%05i  %20s", lost_turn, lost_element, string_error_messages[status].c_str());
				std::cout << buffer << std::endl;
			}
			idx++;
		}
	}
	if (verbose_on) std::cout << get_timestamp() << " end of dynap_xy loop" << std::endl;

	return Status::success;

}

Status::type dynap_ex(
		const Accelerator& accelerator,
		std::vector<Pos<double> >& cod,
		unsigned int nr_turns,
		const Pos<double>& p0,
		unsigned int nrpts_e, double e_min, double e_max,
		unsigned int nrpts_x, double x_min, double x_max,
		bool calculate_closed_orbit,
		std::vector<DynApGridPoint>& grid
	) {

	const std::vector<Element>& the_ring = accelerator.lattice;

	// finds 6D closed-orbit
	if (calculate_closed_orbit) {
		if (verbose_on) {
			std::cout << get_timestamp() << " <" << __FUNCTION__ << ">: calculating closed-orbit...";
			std::cout.flush();
		}
		Status::type status = track_findorbit6(accelerator, cod);
		if (status != Status::success) return status;
		if (verbose_on) {
			std::cout << "ok" << std::endl;
		}
	}

	char buffer[1024];

	// main loop
	if (verbose_on) std::cout << get_timestamp() << " looping over dynap_ex points" << std::endl;
	grid.resize(nrpts_e * nrpts_x);
	int idx = 0;
	for(unsigned int i=0; i<nrpts_e; ++i) {
		double e = e_min + i * (e_max - e_min) / (nrpts_e - 1.0);
		//if (fabs(x) < tiny_amp) x = sgn(x) * tiny_amp;
		for(unsigned int j=0; j<nrpts_x; ++j) {
			double x = x_min + j * (x_max - x_min) / (nrpts_x - 1.0);
			if (fabs(x) < tiny_amp) x = sgn(x) * tiny_amp;
			// prepares initial position
			Pos<double> p = p0;     // offset
			p.de += e; p.rx += x;   // dynapt around closed-orbit
			grid[idx].p = p;      // registers initial condition
			p += cod[0];			// adds closed-orbit
			std::vector<Pos<double> > new_pos;
			int lost_turn = 0, lost_element = 0;
			if (verbose_on) {
				sprintf(buffer, "(%03i,%03i): e=%+11.4E, x=%+11.4E [m] -> ", i+1, j+1, e, x);
				std::cout << buffer; std::cout.flush();
			}
			Status::type status = track_ringpass (accelerator, the_ring, p, new_pos, nr_turns, lost_turn, lost_element, false);
			grid[idx].lost_turn = lost_turn;
			grid[idx].lost_element = lost_element;
			if (verbose_on) {
				sprintf(buffer, "turn=%05i element=%05i  %20s", lost_turn, lost_element, string_error_messages[status].c_str());
				std::cout << buffer << std::endl;
			}
			idx++;
		}
	}
	if (verbose_on) std::cout << get_timestamp() << " end of dynap_ex loop" << std::endl;

	return Status::success;

}
