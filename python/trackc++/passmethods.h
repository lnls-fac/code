#ifndef _PASS_METHODS_H
#define _PASS_METHODS_H

#include "auxiliary.h"
#include "pos.h"

template <typename T> Status::type pm_identity_pass(std::vector<Pos<T> >&pos, const Element &elem);
template <typename T> Status::type pm_drift_pass(std::vector<Pos<T> >&pos, const Element &elem);
template <typename T> Status::type pm_str_mpole_symplectic4_pass(std::vector<Pos<T> >&pos, const Element &elem);
template <typename T> Status::type pm_bnd_mpole_symplectic4_pass(std::vector<Pos<T> >&pos, const Element& elem);
template <typename T> Status::type pm_corrector_pass(std::vector<Pos<T> >&pos, const Element& elem);
template <typename T> Status::type pm_cavity_pass(std::vector<Pos<T> >&pos, const Element &elem);
template <typename T> Status::type pm_thinquad_pass(std::vector<Pos<T> >&pos, const Element &elem);
template <typename T> Status::type pm_thinsext_pass(std::vector<Pos<T> >&pos, const Element &elem);

#include "passmethods.hpp"

#endif
