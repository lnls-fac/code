#include "API.h"

extern size_t g_id;
extern std::vector<FieldMap> g_fieldmaps;

size_t fieldmap_load_fieldmap(const std::string& fname) {
	g_fieldmaps.push_back(FieldMap(g_id, fname));
	return g_id++;
}

void fieldmap_unload_fieldmap(const size_t fieldmap_id) {
	for(size_t i=0; i<g_fieldmaps.size(); ++i) {
		if (g_fieldmaps[i].getid() == fieldmap_id) {
			g_fieldmaps[i].delete_data();
			g_fieldmaps.erase(g_fieldmaps.begin()+i);
			break;
		}
	}
}
