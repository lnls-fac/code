#ifndef _KICKTABLE_H
#define _KICKTABLE_H

#include "auxiliary.h"
#include <string>
#include <vector>



class Kicktable {

	// Kicktable: assumes x_kick and y_kick tables sampled on the same regular (x,y)-point grid.

public:

	std::string         filename;
	double              length;
	unsigned int        x_nrpts, y_nrpts;
	double              x_min, x_max;
	double              y_min, y_max;
	std::vector<double> x_kick,  y_kick;

	Kicktable(const std::string& filename_ = "");
	Status::type load_from_file(const std::string& filename_);
	unsigned int get_idx(unsigned int ix, unsigned int iy) const { return iy*x_nrpts+ix; }

};

Status::type add_kicktable(const std::string& filename, std::vector<Kicktable>& kicktable_list, const Kicktable*& kicktable_pointer);



#endif
