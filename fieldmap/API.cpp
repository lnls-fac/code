#include "API.h"

size_t g_id = 0;
std::vector<FieldMap> g_fieldmaps;

const FieldMap* getfieldmap(const size_t fieldmap_id) {
	for(size_t i=0; i<g_fieldmaps.size(); ++i) {
		if (g_fieldmaps[i].getid() == fieldmap_id) {
			return &(g_fieldmaps[i]);
		}
	}
	return NULL;
}
