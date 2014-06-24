#include "dynap.h"
#include "tracking.h"
#include "lattice.h"
#include "pos.h"
#include <vector>
#include <cfloat>

Status::type dynap_xy(
		const std::vector<Element>& the_ring,
		const unsigned int harmonic_number,
		std::vector<Pos<double> >& orb,
		unsigned int nr_turns,
		const Pos<double>& p0,
		unsigned int nrpts_x, double x_min, double x_max,
		unsigned int nrpts_y, double y_min, double y_max,
		bool calculate_closed_orbit,
		std::vector<DynApPoint> points
	) {

	// finds 6D closed-orbit
	if (calculate_closed_orbit) {
		Status::type status = track_findorbit6(the_ring, harmonic_number, orb);
		if (status != Status::success) return status;
	}

	// main loop
	points.resize(nrpts_x * nrpts_y);
	double tiny_amp = 1e-6; // [m]
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
			points[idx].p = p;      // registers initial condition
			p += orb[0];			// adds closed-orbit
			std::vector<Pos<double> > new_pos;
			int lost_turn = 0, lost_element = 0;
			Status::type status = track_ringpass (the_ring, p, new_pos, nr_turns, lost_turn, lost_element, false);
			points[idx].lost_turn = lost_turn;
			points[idx].lost_element = lost_element;
			fprintf(stdout, "(%03i,%03i): x=%+7.3f,y=%+7.3f [mm] -> %25s turn=%05i element=%05i\n", i+1, j+1, 1e3*x, 1e3*y, string_error_messages[status].c_str(), lost_turn, lost_element);
			idx++;
		}
	}

	return Status::success;

}


