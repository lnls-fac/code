#include <string>
#include <iostream>

#include "API.h"
#include "Vector3D.hpp"
#include "FieldMap.h"

int main() {

	//double energy = 3.0;
	size_t id, nx, nz;
	double x_min, x_max, z_min, z_max;

	try {
		load_fieldmap("fieldmap.txt", id, nx, x_min, x_max, nz, z_min, z_max);
		std::vector<Vector3D<double> > pos;
		std::vector<Vector3D<double> > field;
		pos.push_back(Vector3D<double>(0,0,0));
		pos.push_back(Vector3D<double>(0,0,1.0));
		interpolate_fieldmap(id, pos, field);
		for(size_t i=0; i<field.size(); ++i) {
			std::cout << field[i] << std::endl;
		}
		unload_fieldmap(id);
	} catch (...) {
		std::cout << "error" << std::endl;
	}



//	double si = 0.0;
//	double sf = 1.0;
//	state_type init_state(6);
//	init_state[0] = 0.0; init_state[1] = 0.0; init_state[2] = 0.0;
//	init_state[3] = 0.0; init_state[4] = 0.0; init_state[5] = 1.0;
//	size_t nr_pts = 1000;
//	std::vector<double>     s;
//	std::vector<state_type> trajectory;
//
//	boost_test_integrate_const(energy, fieldmap_id, si, sf, nr_pts, init_state, s, trajectory);
//	for(size_t i=0; i<s.size(); ++i) {
//		std::cout << i << ": " << s[i] << " " << trajectory[i][0] << std::endl;
//	}

	return 0;

}
