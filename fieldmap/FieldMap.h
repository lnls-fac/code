#ifndef FIELD_MAP_H
#define FIELD_MAP_H

#include <string>
#include "Vector3D.hpp"

class FieldMap {

	friend void  load_fieldmap(const std::string& fname, size_t& id, size_t& nx, double& x_min, double& x_max, size_t& nz, double& z_min, double& z_max);
	size_t id;
	size_t nx;
	size_t nz;
	double x_min, dx, x_max;
	double z_min, dz, z_max;
	double *data;
	std::string fname;

public:

	FieldMap(size_t id_, const std::string& fname_);

	size_t       getid() const { return this->id; }
	size_t       ix(const double& x) const;
	size_t       iz(const double& z) const;
	double		 x(size_t ix) const;
	double		 z(size_t iz) const;
	Vector3D<double> pos(size_t ix, size_t iy) const;
	Vector3D<double> field(const Vector3D<double>& pos) const;
	void         delete_data();

private:

	void read_fieldmap_from_file(const std::string& fname_);

};



#endif
