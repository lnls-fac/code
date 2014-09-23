
//
// C++ Interface: %{MODULE}
//
// Description: 
//
//
// Author: %{AUTHOR} <%{EMAIL}>, (C) %{YEAR}
//
// Copyright: See COPYING file that comes with this distribution
//
//

/* Tracy-3

   J. Bengtsson, BNL 2007

   ORDER   1   link to the linear TPSA (nv_tps = 1)
          >1   link to Berz' TPSA

*/

// C standard library
#include <stdio.h>
#include <stdint.h>
#include <stddef.h>
#include <setjmp.h>
#include <time.h>
#include <memory.h>
#if !defined(__APPLE__)
#include <malloc.h>
#endif
//#include <execinfo.h>


// C++ standard library
#include <cstdlib>
#include <cfloat>
#include <cctype>
#include <cmath>
#include <iostream>
#include <sstream>
#include <iomanip>
#include <fstream>
using namespace std;

#ifndef ORDER
#define ORDER 1
#endif 

// Tracy-3
#include "field.h"
#include "mathlib.h"

#if ORDER == 1
  // linear TPSA
  #include "tpsa_lin.h"
  #include "tpsa_lin_pm.h"
#else
  // interface to M. Berz' TPSA
  #include "tpsa_for.h"
  #include "tpsa_for_pm.h"
#endif

#include "tracy.h"
#include "tracy_global.h"
#include "ety.h"

#include "num_rec.h"

#include "radia2tracy.h"
#include "pascalio.h"

#include "t2elem.h"
#include "t2cell.h"
#include "t2lat.h"
#include "t2ring.h"

#include "fft.h"

#include "physlib.h"
#include "nsls-ii_lib.h"


#include "lsoc.h"

#include "naffutils.h"

#include "soleillib.h"

#include "modnaff.h"

#include "rdmfile.h"
#include "prtmfile.h"

#include "nsls-ii_lib.h"

#include "max4_lib.h"
//#include "soleilcommon.h"
#include "read_script.h"

#include "libs/tracking_mp/tracking_mp.h"
#include "lnlscommon.h"


// Truncated Power Series Algebra (TPSA)
extern const int  nv_tps, nd_tps, ndpt_tps, iref_tps;
extern int        no_tps;
extern double     eps_tps;

extern ElemFamType ElemFam[];

extern CellType Cell[];

extern globvalrec globval;


