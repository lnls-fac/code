#include <cmath>
#include <vector>
#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <cstdlib>
#include <set>

#include "FieldMap.h"

FieldMap::FieldMap(const std::string& fname_) :
		nx(0), nz(0),
		x_min(0), x_max(0),
		z_min(0), z_max(0),
		data(0)
{
	this->read_fieldmap_from_file(fname_);
}

FieldMap::~FieldMap()
{
	delete [] data;
}


void FieldMap::read_fieldmap_from_file(const std::string& fname_)
{

	const size_t capacity_inc = 10 * 1000;

	// opens file
	std::ifstream file("fmap.txt");
	if (!file.is_open()) {
		return;
	}

	// reads header section
	std::string word, line;
	file >> word; std::string nome_do_mapa; std::getline(file, nome_do_mapa);
	file >> word; std::string data_hora;    std::getline(file, data_hora);
	file >> word; std::string nome_arquivo; std::getline(file, nome_arquivo);
	file >> word; std::string nr_imas; 		std::getline(file, nr_imas);
	file >> word; std::string nome_ima;		std::getline(file, nome_ima);
	file >> word; std::string gap;  		std::getline(file, gap);
	file >> word; std::string gap_controle;	std::getline(file, gap_controle);
	file >> word; std::string comprimento;	std::getline(file, comprimento);
	file >> word; std::string corrente;		std::getline(file, corrente);
	file >> word; std::string centro_pos_z;	std::getline(file, centro_pos_z);
	file >> word; std::string centro_pos_x;	std::getline(file, centro_pos_x);
	file >> word; std::string rotacao;		std::getline(file, rotacao);
	std::getline(file, line); //std::cout << line << std::endl;
	std::getline(file, line); //std::cout << line << std::endl;
	std::getline(file, line); //std::cout << line << std::endl;

	// reads data section
	std::set<double> x_set, y_set, z_set;
	double x,y,z,bx,by,bz;
	size_t nr_points = 0;
	size_t capacity  = 0;
	if (this->data != 0) { delete [] this->data; } // deallocates memory if already set
	while (true) {
		if (nr_points >= capacity) {
			// reallocates more data space
			capacity += capacity_inc;
			this->data = (double*) std::realloc(this->data, capacity*3*sizeof(double));
		}
		file >> x >> y >> z >> bx >> by >> bz;
		data[3*nr_points+0] = bx;
		data[3*nr_points+1] = by;
		data[3*nr_points+2] = bz;
		if (file.eof()) break;
		x_set.insert(x); y_set.insert(y); z_set.insert(z);
		nr_points++;
	}
	// updates object properties
	this->fname = fname_;
	this->data  = (double*) std::realloc(this->data, nr_points*3*sizeof(double));
	this->nx    = x_set.size();
	this->nz    = z_set.size();
	this->x_min = *(x_set.begin());
	this->x_max = *(x_set.rbegin());
	this->z_min = *(z_set.begin());
	this->z_max = *(z_set.rbegin());
	// throws exception in case dimensions do not agree
	if (nr_points != (this->nx * this->nz * y_set.size())) {
		throw FieldMapException::inconsistent_dimensions;
	}

	std::cout << "nr.points       : " << nr_points    << std::endl;
	std::cout << "nr.points.x_set : " << this->nx     << std::endl;
	std::cout << "nr.points.y_set : " << y_set.size() << std::endl;
	std::cout << "nr.points.z_set : " << this->nz     << std::endl;
	std::cout << "min.x           : " << this->x_min  << std::endl;
	std::cout << "max.x           : " << this->x_max  << std::endl;
	std::cout << "min.z           : " << this->z_min  << std::endl;
	std::cout << "max.z           : " << this->z_max  << std::endl;

	file.close();

}

Vector3D<double> FieldMap::field(const Vector3D<double>& pos) const
{

	// checks range
	if (pos.x < this->x_min) {
		throw FieldMapException::out_of_range_x_min;
	}
	if (pos.x > this->x_max) {
		throw FieldMapException::out_of_range_x_max;
	}
	if (pos.z < this->z_min) {
		throw FieldMapException::out_of_range_z_min;
	}
	if (pos.z > this->x_max) {
		throw FieldMapException::out_of_range_z_max;
	}

	// calcs indices
	size_t ix1  = (size_t) (this->nx * (pos.x - this->x_min) / (this->x_max - this->x_min));
	size_t iz1  = (size_t) (this->nz * (pos.z - this->z_min) / (this->z_max - this->z_min));
	size_t ix2  = (ix1 == this->nx) ? ix1 : ix1 + 1;
	size_t iz2  = (iz1 == this->nz) ? iz1 : iz1 + 1;
	// gets field on grid points
	//      point1: (iz1, ix1), point2: (iz1, ix2), point3: (iz2, ix1), point4: (iz2, ix2)
	size_t p1 = iz1 * this->nx + ix1;
	size_t p2 = iz1 * this->nx + ix2;
	size_t p3 = iz2 * this->nx + ix1;
	size_t p4 = iz2 * this->nx + ix2;
	double x1  = this->x_min + ix1 * (this->x_max - this->)
	double bx1 = this->data[3*p1+0], by1 = this->data[3*p1+1], bz1 = this->data[3*p1+2];
	double bx2 = this->data[3*p2+0], by2 = this->data[3*p2+1], bz2 = this->data[3*p2+2];
	double bx3 = this->data[3*p3+0], by3 = this->data[3*p3+1], bz2 = this->data[3*p3+2];
	double bx4 = this->data[3*p4+0], by4 = this->data[3*p4+1], bz2 = this->data[3*p4+2];

	// linear iterpolation: first along z then along z
	bx_step1 = pos.x
	Vector3D<double> f = Vector3D<double>();
}
