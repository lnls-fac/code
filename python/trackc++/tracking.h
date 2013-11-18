#ifndef _TRACKING_H
#define _TRACKING_H

#include "auxiliary.h"

template <typename T>
Status::type track1turn(const std::vector<Element>& lattice, std::vector<Pos<T> >& pos) {

	Status::type status;

	for(int i=0; i<lattice.size(); ++i) {
		const Element& element = lattice[i];
		switch (lattice[i].pass_method) {
			case PassMethod::pm_identity_pass:
				if ((status = pm_identity_pass<T>(pos, element)) != Status::success) return status;
				break;
			case PassMethod::pm_drift_pass:
				if ((status = pm_drift_pass<T>(pos, element)) != Status::success) return status;
				break;
			case PassMethod::pm_str_mpole_symplectic4_pass:
				if ((status = pm_str_mpole_symplectic4_pass<T>(pos, element)) != Status::success) return status;
				break;
			case PassMethod::pm_bnd_mpole_symplectic4_pass:
				if ((status = pm_bnd_mpole_symplectic4_pass<T>(pos, element)) != Status::success) return status;
				break;
			case PassMethod::pm_corrector_pass:
				if ((status = pm_corrector_pass<T>(pos, element)) != Status::success) return status;
				break;
			case PassMethod::pm_cavity_pass:
				if ((status = pm_cavity_pass<T>(pos, element)) != Status::success) return status;
				break;
			case PassMethod::pm_thinquad_pass:
				if ((status = pm_thinquad_pass<T>(pos, element)) != Status::success) return status;
				break;
			case PassMethod::pm_thinsext_pass:
				if ((status = pm_thinsext_pass<T>(pos, element)) != Status::success) return status;
				break;
			default:
				return Status::passmethod_not_defined;
		}
	}

	return Status::success;

}

#endif
