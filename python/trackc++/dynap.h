#ifndef _DYNAP_H
#define _DYNAP_H

#include "pos.h"
#include "auxiliary.h"
#include <vector>


struct DynApPoint {
	Pos<double> p;
	unsigned int lost_turn;
	unsigned int lost_element;
};

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
	);

#endif
