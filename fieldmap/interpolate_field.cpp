#include "API.h"

extern size_t g_id;
extern std::vector<FieldMap> g_fieldmaps;

int fieldmap_interpolate_field(const size_t fieldmap_id, const std::vector<Vector3D<double> >& pos, std::vector<Vector3D<double> >& field) {

	const FieldMap* fieldmap = getfieldmap(fieldmap_id);
	if (fieldmap == NULL) {

	}
	for(size_t i=0; i<pos.size(); ++i) {
		Vector3D<double> b = fieldmap->field(pos[i]);
		field.push_back(b);
	}

	return 0;

}
