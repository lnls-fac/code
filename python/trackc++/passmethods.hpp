#ifndef _PASS_METHOD_AT_H
#define _PASS_METHOD_AT_H


#include "auxiliary.h"
#include "pos.h"
#include "elements.h"
#include "passmethods.h"

// constants for 4th-order symplectic integrator
#define DRIFT1 ( 0.6756035959798286638e00)
#define DRIFT2 (-0.1756035959798286639e00)
#define KICK1  ( 0.1351207191959657328e01)
#define KICK2  (-0.1702414383919314656e01)

template <typename T>
void drift(std::vector<Pos<T> > &pos, const double& length) {
	for(unsigned int p=0; p<pos.size(); ++p) {
		T &rx = pos[p].rx, &px = pos[p].px, &ry = pos[p].ry, &py = pos[p].py, &de = pos[p].de, &dl = pos[p].dl;
        T pnorm = 1 / (1 + de);
        T norml = length * pnorm;
        rx += norml * px;
        ry += norml * py;
        dl += 0.5 * norml * pnorm * (px*px + py*py);
	}
}

template <typename T>
void calcpolykick(const Pos<T> &pos, const std::vector<double>& polynom_a, const std::vector<double>& polynom_b, T& real_sum, T& imag_sum) {
	int n = polynom_b.size();
	real_sum = polynom_b[n-1];
    imag_sum = polynom_a[n-1];
    for(unsigned int i=n-2;i>=0;--i) {
        T real_sum_tmp = real_sum * pos.rx - imag_sum * pos.ry + polynom_b[i];
        imag_sum = imag_sum * pos.rx + real_sum * pos.ry + polynom_a[i];
        real_sum = real_sum_tmp;
    }
}


template <typename T>
void fastdrift(Pos<T> &pos, const double& norml) {
	T dx = norml * pos.px;
    T dy = norml * pos.py;
    pos.rx += dx;
    pos.ry += dy;
    pos.dl += 0.5 * norml * (pos.px*pos.px + pos.py*pos.py) / (1 + pos.de);
}

template <typename T>
void strthinkick(Pos<T>& pos, const double& length, const std::vector<double>& polynom_a, const std::vector<double>& polynom_b) {
        T real_sum, imag_sum;
		calcpolykick<T>(pos, polynom_a, polynom_b, real_sum, imag_sum);
        pos.px -= length * real_sum;
        pos.py += length * imag_sum;
}


template <typename T>
void global_2_local(std::vector<Pos<T> > &pos, const Element &elem) {

	double ty = std::tan(elem.err_yaw);
	double tp = std::tan(elem.err_pitch);
	double c  = std::cos(elem.err_roll);
	double s  = std::sin(elem.err_roll);

	for(unsigned int p=0; p<pos.size(); ++p) {
		T &rx = pos[p].rx, &px = pos[p].px, &ry = pos[p].ry, &py = pos[p].py;
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
		T &rx = pos[p].rx, &px = pos[p].px, &ry = pos[p].ry, &py = pos[p].py;
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
	drift<T>(pos, elem.length);
	return Status::success;
}

template <typename T>
Status::type pm_str_mpole_symplectic4_pass(std::vector<Pos<T> >&pos, const Element &elem) {

	global_2_local(pos, elem);

	double sl = elem.length / float(elem.nr_steps);
	double l1 = sl * DRIFT1;
	double l2 = sl * DRIFT2;
	double k1 = sl * KICK1;
	double k2 = sl * KICK2;
	const std::vector<double> &polynom_a = elem.polynom_a;
	const std::vector<double> &polynom_b = elem.polynom_b;
	for(unsigned int p=0; p<pos.size(); ++p) {
		T &de = pos[p].de;
		for(unsigned int i=0; i<elem.nr_steps; ++i) {
			T norm   = 1/(1 + de);
	        T norml1 = l1 * norm;
	        T norml2 = l2 * norm;
	        fastdrift(pos[p], norml1);
	        strthinkick<T>(pos[p], k1, polynom_a, polynom_b);
	        fastdrift<T>(pos[p], norml2);
	        strthinkick<T>(pos[p], k2, polynom_a, polynom_b);
	        fastdrift<T>(pos[p], norml2);
	        strthinkick<T>(pos[p], k1, polynom_a, polynom_b);
	        fastdrift<T>(pos[p], norml1);
		}
	}

	local_2_global(pos, elem);

	return Status::success;
}

template <typename T>
Status::type pm_bnd_mpole_symplectic4_pass(std::vector<Pos<T> >&pos, const Element &elem) {
	return Status::passmethod_not_implemented;
}

template <typename T>
Status::type pm_corrector_pass(std::vector<Pos<T> >&pos, const Element &elem) {
	global_2_local(pos, elem);
	const double& xkick = elem.hkick;
	const double& ykick = elem.vkick;
	if (elem.length == 0) {
		for(unsigned int p=0; p<pos.size(); ++p) {
			T &px = pos[p].px, &py = pos[p].py;
			px += xkick;
			py += ykick;
		}
	} else {
		for(unsigned int p=0; p<pos.size(); ++p) {
			T &rx = pos[p].rx, &px = pos[p].px, &ry = pos[p].ry, &py = pos[p].py, &de = pos[p].de, &dl = pos[p].dl;
			T pnorm   = 1 / (1 + de);
			T norml   = elem.length * pnorm;
			dl += norml * pnorm * 0.5 * (
					xkick * xkick/3.0 + ykick * ykick/3.0 +
				    px*px + py*py +
				    px * xkick + py * ykick
				  );
			rx += norml * (px + 0.5 * xkick);
			px += xkick;
			ry += norml * (py + 0.5 * ykick);
			py += ykick;
		}
	}
	local_2_global(pos, elem);
	return Status::success;
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
