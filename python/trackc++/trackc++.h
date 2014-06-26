#ifndef _TRACKCPP_H
#define _TRACKCPP_H

// TRACKC++
// ========
// Author: 		Ximenes R. Resende
// email:  		xresende@gmail.com, ximenes.resende@lnls.br
// affiliation:	LNLS - Laboratorio Nacional de Luz Sincrotron
// Date: 		Tue Dec 10 17:57:20 BRST 2013

#define ATCOMPATIBLE 1

#include "commands.h"
#include "optics.h"
#include "dynap.h"
#include "tracking.h"
#include "lattice.h"
#include "passmethods.h"
#include "pos.h"
#include "elements.h"
#include "auxiliary.h"
#include "tpsa.h"

void sirius_v500(std::vector<Element>& the_ring);

#endif
