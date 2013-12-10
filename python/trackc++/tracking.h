#ifndef _TRACKING_H
#define _TRACKING_H

// TRACKC++
// ========
// Author: 		Ximenes R. Resende
// email:  		xresende@gmail.com, ximenes.resende@lnls.br
// affiliation:	LNLS - Laboratorio Nacional de Luz Sincrotron
// Date: 		Tue Dec 10 17:57:20 BRST 2013

#include "trackc++.h"

template <typename T>
Status::type linepass (const std::vector<Element>& lattice, std::vector<Pos<T> >& orig_pos, std::vector<Pos<T> >& pos, int *element_idx, bool trajectory) {

	Status::type status;

	int nr_elements  = lattice.size();
	int nr_particles = orig_pos.size();

	for(int i=0; i<nr_elements; ++i) {

		*element_idx = i;
		const Element& element = lattice[i];

		// records trajectory at entrance of element
		if (trajectory) {
			for(int j=0; j<nr_particles;++j) {
				pos.push_back(orig_pos[j]);
			}
		}

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
		//std::cout << " " << pos[0].rx << std::endl;

	}
	for(int j=0; j<nr_particles;++j) {
		pos.push_back(orig_pos[j]);
	}

	return Status::success;

}


template <typename T>
Status::type ringpass (const std::vector<Element>& lattice, std::vector<Pos<T> >& orig_pos, std::vector<Pos<T> >& pos, const int nr_turns, int *turn_idx, int *element_idx) {

	Status::type status;

	for(int n=0; n<nr_turns; ++n) {
		*turn_idx = n;
		std::vector<Pos<T> > tmp_pos;
		if ((status = linepass (lattice, orig_pos, tmp_pos, element_idx, false)) != Status::success) return status;
		// records turn-by-turn data
		for(int j=0; j<tmp_pos.size();++j) {
			pos.push_back(orig_pos[j]);
		}
	}
	return Status::success;
}






#endif
