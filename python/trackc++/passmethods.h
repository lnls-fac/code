#ifndef _PASS_METHODS_H
#define _PASS_METHODS_H

// TRACKC++
// ========
// Author: 		Ximenes R. Resende
// email:  		xresende@gmail.com, ximenes.resende@lnls.br
// affiliation:	LNLS - Laboratorio Nacional de Luz Sincrotron
// Date: 		Tue Dec 10 17:57:20 BRST 2013

#include "auxiliary.h"
#include "pos.h"

template <typename T> Status::type pm_identity_pass              (Pos<T> &pos, const Element &elem);
template <typename T> Status::type pm_drift_pass                 (Pos<T> &pos, const Element &elem);
template <typename T> Status::type pm_str_mpole_symplectic4_pass (Pos<T> &pos, const Element &elem, bool radiation);
template <typename T> Status::type pm_bnd_mpole_symplectic4_pass (Pos<T> &pos, const Element &elem, bool radiation);
template <typename T> Status::type pm_corrector_pass             (Pos<T> &pos, const Element &elem);
template <typename T> Status::type pm_cavity_pass                (Pos<T> &pos, const Element &elem);
template <typename T> Status::type pm_thinquad_pass              (Pos<T> &pos, const Element &elem);
template <typename T> Status::type pm_thinsext_pass              (Pos<T> &pos, const Element &elem);

#include "passmethods.hpp"

#endif
