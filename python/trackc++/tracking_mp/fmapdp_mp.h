// FMAPDP_MP
// =========
// Rotina que paraleliza o cálculo de abertura dinâmica 'fmapdp' com análise NAFF
//
// 2012-08-20	Ximenes R. Resende


#ifndef FMAPDP_MP_H
#define FMAPDP_MP_H

#include <stdlib.h>

//#include "../../tracy_lib.h"
//#include "../../soleilcommon.h"
//#include "../../naffutils.h"
//extern globvalrec globval;


#include "mp_task_mgr.h"

void fmapdp_mp(int nr_cpus, long Nbx, long Nbe, long Nbtour, double x0, double xmax,
		double emin, double emax, double z, bool diffusion);


#endif

