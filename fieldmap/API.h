#ifndef FIELDMAP_API_H
#define FIELDMAP_API_H

#include <vector>
#include "Vector3D.hpp"
#include "FieldMap.h"

struct FieldMapException {
	enum type {
		success                       = 0,
		inconsistent_dimensions       = 1,
		out_of_range_x_min            = 2,
		out_of_range_x_max            = 3,
		out_of_range_z_min            = 4,
		out_of_range_z_max            = 5,
		file_not_found                = 6
	};
};

typedef std::vector<double> state_type;
const FieldMap* getfieldmap(const size_t fieldmap_id);


void boost_integrate_const(
		const double& energy,
		const FieldMap& fieldmap,
		const double& si, const double& sf, size_t nr_pts, state_type& init_state,
		std::vector<double>& s, std::vector<state_type>& trajectory);

void   load_fieldmap(const std::string& fname, size_t& id, size_t& nx, double& x_min, double& x_max, size_t& nz, double& z_min, double& z_max);
void   unload_fieldmap(const size_t fieldmap_id);
int    interpolate_fieldmap(const size_t fieldmap_id, const std::vector<Vector3D<double> >& pos, std::vector<Vector3D<double> >& field);
size_t nr_fieldmaps();
void   clear();
void   boost_integrate_const(
		const double& energy,
		const FieldMap& fieldmap,
		const double& si, const double& sf, size_t nr_pts, state_type& init_state,
		std::vector<double>& s, std::vector<state_type>& trajectory);


#endif
