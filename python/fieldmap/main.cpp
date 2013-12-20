#include <string>

#include "FieldMap.h"
#include "Vector3D.h"

int main() {

	FieldMap fm("fieldmap.txt");

	Vector3D<> field = fm.field(Vector3D<double>(0,0,0));

	return 0;

}
