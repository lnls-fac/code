#include "API.h"

extern size_t g_id;
extern std::vector<FieldMap> g_fieldmaps;

void  load_fieldmap(const std::string& fname, size_t& id, size_t& nx, double& x_min, double& x_max, size_t& nz, double& z_min, double& z_max) {
	FieldMap fieldmap(fname, g_id);
	g_fieldmaps.push_back(fieldmap);
	id    = g_id;
	nx    = g_fieldmaps.rbegin()->nx;
	x_min = g_fieldmaps.rbegin()->x_min;
	x_max = g_fieldmaps.rbegin()->x_max;
	nz    = g_fieldmaps.rbegin()->nz;
	z_min = g_fieldmaps.rbegin()->z_min;
	z_max = g_fieldmaps.rbegin()->z_max;
	g_id++;
}

void unload_fieldmap(const size_t fieldmap_id) {
	for(size_t i=0; i<g_fieldmaps.size(); ++i) {
		if (g_fieldmaps[i].getid() == fieldmap_id) {
			g_fieldmaps[i].delete_data();
			g_fieldmaps.erase(g_fieldmaps.begin()+i);
			break;
		}
	}
}


