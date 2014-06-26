#ifndef _FLAT_FILE_H
#define _FLAT_FILE_H

#include "elements.h"
#include "auxiliary.h"
#include <string>
#include <vector>

struct FlatFileType {
		enum type_ {
			marker    = -1,
			drift     =  0,
			mpole     =  1,
			cavity    =  2,
			corrector =  3,
			thin_kick =  3,
			insertion =  6
		};
	};


Status::type read_flat_file_tracy(const std::string& filename, std::vector<Element>& the_ring);
void read_polynomials(std::ifstream& fp, Element& e);

#endif
