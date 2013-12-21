#include <string>

#include "FieldMap.h"
#include "Vector3D.h"
#include <iostream>

int main() {

	FieldMap fm("fieldmap.txt");


	std::cout << fm.x(0) << std::endl;
	std::cout << fm.x(100) << std::endl;
	std::cout << fm.ix(-100) << std::endl;
	std::cout << fm.ix(12) << std::endl;

	std::cout << "begin" << std::endl;
	int nr = 20000000;
	double a=0;
	for (int i=0; i<nr; ++i) {
		Vector3D<double> pos(-20.0*i/nr,0,100.0*i/nr);
		Vector3D<> field = fm.field(pos);
		a += field.y;
	}
	//std::cout << field << std::endl;
	std::cout << "end" << std::endl;
	std::cout << a << std::endl;
	return 0;

}
