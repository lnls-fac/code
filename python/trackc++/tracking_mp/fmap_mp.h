// FMAP_MP
// =======
// Rotina que paraleliza o cálculo de abertura dinâmica 'fmap' com análise NAFF
//
// 2012-08-20	Ximenes R. Resende


#ifndef FMAP_MP_H
#define FMAP_MP_H

#include <stdlib.h>

//#include "../../tracy_lib.h"
//#include "../../soleilcommon.h"
//#include "../../naffutils.h"
//extern globvalrec globval;

#include "mp_task_mgr.h"

void fmap_mp(int nr_cpus, long Nbx, long Nbz, long Nbtour, double x0, double xmax,
		  double z0, double zmax, double energy, bool diffusion);


#endif

