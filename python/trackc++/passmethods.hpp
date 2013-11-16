#ifndef _PASS_METHOD_AT_H
#define _PASS_METHOD_AT_H


#include <cmath>
#include <vector>
#include "pos.h"
#include "elements.h"
#include "passmethods.h"

// constants for 4th-order symplectic integrator
#define DRIFT1 ( 0.6756035959798286638e00)
#define DRIFT2 (-0.1756035959798286639e00)
#define KICK1  ( 0.1351207191959657328e01)
#define KICK2  (-0.1702414383919314656e01)


template <typename T>
void global_2_local(std::vector<Pos<T> > &pos, const Element &elem) {

	double ty = std::tan(elem.err_yaw);
	double tp = std::tan(elem.err_pitch);
	double c  = std::cos(elem.err_roll);
	double s  = std::sin(elem.err_roll);

	for(unsigned int p=0; p<pos.size(); ++p) {
		T &rx = pos[p].rx, &px = pos[p].px, &ry = pos[p].ry, &py = pos[p].py, &de = pos[p].de, &dl = pos[p].dl;
		// misalignment x and y
		rx += - elem.err_dx;
		ry += - elem.err_dy;
		// yaw error
		rx += - ty * (elem.length / 2);
		px += + ty;
		// pitch error
		ry += - tp * (elem.length / 2);
		py += + tp;
		// roll error
		T rx0 = rx; T ry0 = ry;
		T px0 = px; T py0 = py;
		rx =  c * rx0 + s * ry0;
		ry = -s * rx0 + c * ry0;
		px =  c * px0 + s * py0;
		py = -s * px0 + c * py0;
	};
};

template <typename T>
void local_2_global(std::vector<Pos<T> > &pos, const Element &elem) {

	double c  = std::cos(elem.err_roll);
	double s  = std::sin(elem.err_roll);
	double tp = std::tan(elem.err_pitch);
	double ty = std::tan(elem.err_yaw);

	for(unsigned int p=0; p<pos.size(); ++p) {
		T &rx = pos[p].rx, &px = pos[p].px, &ry = pos[p].ry, &py = pos[p].py, &de = pos[p].de, &dl = pos[p].dl;
		// roll error
		T rx0 = rx; T ry0 = ry;
		T px0 = px; T py0 = py;
		rx =  c * rx0 - s * ry0;
		ry =  s * rx0 + c * ry0;
		px =  c * px0 - s * py0;
		py =  s * px0 + c * py0;
		// pitch error
		ry += + tp * (elem.length / 2);
		py += - tp;
		// yaw error
		rx += + ty * (elem.length / 2);
		px += - ty;
		// misalignment x and y
		rx += + elem.err_dx;
		ry += + elem.err_dy;
	};
};



template <typename T>
Status::type pm_identity_pass(std::vector<Pos<T> >&pos, const Element &elem) {
	return Status::success;
}

template <typename T>
Status::type pm_drift_pass(std::vector<Pos<T> >&pos, const Element &elem) {
	return Status::passmethod_not_implemented;
}

template <typename T>
Status::type pm_str_mpole_symplectic4_pass(std::vector<Pos<T> >&pos, const Element &elem) {
	return Status::passmethod_not_implemented;
}

template <typename T>
Status::type pm_bnd_mpole_symplectic4_pass(std::vector<Pos<T> >&pos, const Element &elem) {
	return Status::passmethod_not_implemented;
}

template <typename T>
Status::type pm_corrector_pass(std::vector<Pos<T> >&pos, const Element &elem) {
	return Status::passmethod_not_implemented;
}

template <typename T>
Status::type pm_cavity_pass(std::vector<Pos<T> >&pos, const Element &elem) {
	return Status::passmethod_not_implemented;
}

template <typename T>
Status::type pm_thinquad_pass(std::vector<Pos<T> >&pos, const Element &elem) {
	return Status::passmethod_not_implemented;
}

template <typename T>
Status::type pm_thinsext_pass(std::vector<Pos<T> >&pos, const Element &elem) {
	return Status::passmethod_not_implemented;
}

#undef DRIFT1
#undef DRIFT2
#undef KICK1
#undef KICK2


#endif
