#ifndef _OUTPUT_H
#define _OUTPUT_H

#include "dynap.h"
#include "accelerator.h"
#include "elements.h"
#include <vector>
#include <string>
#include <cstdlib>

Status::type print_closed_orbit    (const Accelerator& accelerator, const std::vector<Pos<double>>&    cod,  const std::string& filename = "cod_out.txt");
Status::type print_dynapgrid       (const Accelerator& accelerator, const std::vector<DynApGridPoint>& grid, const std::string& filename = "dynap_out.txt");
void         print_header          (FILE* fp);

#endif
