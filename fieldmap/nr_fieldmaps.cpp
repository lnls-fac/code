#include "API.h"

//extern size_t g_id;
extern std::vector<FieldMap> g_fieldmaps;

size_t  nr_fieldmaps()
{
	return g_fieldmaps.size();
}
