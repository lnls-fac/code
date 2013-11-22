#ifndef _TRACKING_H
#define _TRACKING_H

#include "trackc++.h"

template <typename T>
Status::type track1turn(const std::vector<Element>& lattice, std::vector<Pos<T> >& orig_pos, std::vector<Pos<T> >& pos, int *element_idx, bool trajectory) {

	Status::type status;

	int nr_elements  = lattice.size();
	int nr_particles = orig_pos.size();

	for(int i=0; i<nr_elements; ++i) {
		*element_idx = i;
		const Element& element = lattice[i];
		switch (lattice[i].pass_method) {
			case PassMethod::pm_identity_pass:
				if ((status = pm_identity_pass<T>(orig_pos, element)) != Status::success) return status;
				break;
			case PassMethod::pm_drift_pass:
				if ((status = pm_drift_pass<T>(orig_pos, element)) != Status::success) return status;
				break;
			case PassMethod::pm_str_mpole_symplectic4_pass:
				//break;
				if ((status = pm_str_mpole_symplectic4_pass<T>(orig_pos, element)) != Status::success) return status;
				break;
			case PassMethod::pm_bnd_mpole_symplectic4_pass:
				//break;
				if ((status = pm_bnd_mpole_symplectic4_pass<T>(orig_pos, element)) != Status::success) return status;
				break;
			case PassMethod::pm_corrector_pass:
				//break;
				if ((status = pm_corrector_pass<T>(orig_pos, element)) != Status::success) return status;
				break;
			case PassMethod::pm_cavity_pass:
				//break;
				if ((status = pm_cavity_pass<T>(orig_pos, element)) != Status::success) return status;
				break;
			case PassMethod::pm_thinquad_pass:
				if ((status = pm_thinquad_pass<T>(orig_pos, element)) != Status::success) return status;
				break;
			case PassMethod::pm_thinsext_pass:
				if ((status = pm_thinsext_pass<T>(orig_pos, element)) != Status::success) return status;
				break;
			default:
				return Status::passmethod_not_defined;
		}
		if (trajectory || (i == nr_elements-1)) {
			for(int j=0; j<nr_particles;++j) {
				pos.push_back(orig_pos[j]);
			}
		}
		//std::cout << " " << pos[0].rx << std::endl;
	}

	return Status::success;

}

#endif
