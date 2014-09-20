// FMAP_MP
// =======
// Rotina que paraleliza o cálculo de abertura dinâmica 'daxy'
//
// 2014-06-16	Ximenes R. Resende


#ifndef DAEX_MP_H
#define DAEX_MP_H

#include <stdlib.h>

#include "../../tracy_lib.h"
#include "../../soleilcommon.h"
#include "../../naffutils.h"
extern globvalrec globval; 

#include "mp_task_mgr.h"

void daex_mp(int nr_cpus, long Nbx, long Nbe, long Nbtour, double e0, double emax, double x0, double xmax,  double z0);

#endif

