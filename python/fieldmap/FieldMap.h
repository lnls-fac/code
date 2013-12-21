#ifndef FIELD_MAP_H
#define FIELD_MAP_H

struct FieldMapException {
	enum type {
		success                       = 0,
		inconsistent_dimensions       = 1,
		out_of_range_x_min            = 2,
		out_of_range_x_max            = 3,
		out_of_range_z_min            = 4,
		out_of_range_z_max            = 5,
	};
};


#include <string>
#include "Vector3D.h"

class FieldMap {

	int    nx;
	int    nz;
	double x_min, x_max;
	double z_min, z_max;
	double *data;
	std::string fname;

public:

	FieldMap(const std::string& fname_);
	~FieldMap();

	double		 dx() const { return (this->x_max - this->x_min)/this->nx; }
	double		 dz() const { return (this->z_max - this->z_min)/this->nz; }
	size_t           ix(const double& x) const;
	size_t           iz(const double& z) const;
	double		 x(size_t ix) const;
	double		 z(size_t iz) const;
	Vector3D<double> pos(size_t ix, size_t iy) const;
	Vector3D<double> field(const Vector3D<double>& pos) const;

private:

	void read_fieldmap_from_file(const std::string& fname_);

};

#endif
