#ifndef _TRACKING_H
#define _TRACKING_H

// TRACKC++
// ========
// Author: 		Ximenes R. Resende
// email:  		xresende@gmail.com, ximenes.resende@lnls.br
// affiliation:	LNLS - Laboratorio Nacional de Luz Sincrotron
// Date: 		Tue Dec 10 17:57:20 BRST 2013

#include "trackc++.h"

// linepass
// --------
// tracks particles along a beam transport line
//
// inputs:
//		line:	 		Element vector representing the beam transport line
//		orig_pos:		Pos vector representing initial positions of particles
//		element_idx:	equivalent to shifting the lattice so that '*element_idx' is the index for the first element
//		trajectory:		flag indicating that trajectory is to be recorded at entrance of all elements
//						(otherwise only the coordinates at the exit of last element is recorded)
// outputs:
//		pos:			Pos vector of particles' final coordinates (or trajetory)
//		element_idx:	in case of problems with passmethods, '*element_idx' is the index of the corresponding element
//		RETURN:			status do tracking (see 'auxiliary.h')

template <typename T>
Status::type linepass (const std::vector<Element>& line, std::vector<Pos<T> >& orig_pos, std::vector<Pos<T> >& pos, int *element_idx, bool trajectory) {

	Status::type status = Status::success;

	int nr_elements  = line.size();
	int nr_particles = orig_pos.size();

	for(int i=0; i<nr_elements; ++i) {

		const Element& element = line[*element_idx];

		// records trajectory at entrance of element
		if (trajectory) {
			for(int j=0; j<nr_particles;++j) {
				pos.push_back(orig_pos[j]);
			}
		}

		switch (line[i].pass_method) {
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

		*element_idx = (*element_idx + 1) % nr_elements;

	}
	for(int j=0; j<nr_particles;++j) {
		pos.push_back(orig_pos[j]);
	}

	return status;

}

// ringpass
// --------
// tracks particles around a ring
//
// inputs:
//		ring: 			Element vector representing the ring
//		orig_pos:		Pos vector representing initial positions of particles
//		element_idx:	equivalent to shifting the lattice so that '*element_idx' is the index for the first element
//		nr_turns:		number of turns for tracking
//
// outputs:
//		pos:			Pos vector of particles' coordinates of the turn_by_turn data (at end of the ring at each turn)
//		turn_idx:		in case of problems with passmethods, '*turn_idx' is the index of the corresponding turn
//		element_idx:	in case of problems with passmethods, '*element_idx' is the index of the corresponding element
//		RETURN:			status do tracking (see 'auxiliary.h')


template <typename T>
Status::type ringpass (const std::vector<Element>& ring, std::vector<Pos<T> >& orig_pos, std::vector<Pos<T> >& pos, const int nr_turns, int *turn_idx, int *element_idx) {

	Status::type status  = Status::success;

	*turn_idx = 0;
	for(int n=0; n<nr_turns; ++n) {
		std::vector<Pos<T> > tmp_pos;
		if ((status = linepass (ring, orig_pos, tmp_pos, element_idx, false)) != Status::success) return status;
		// records turn-by-turn data
		for(int j=0; j<tmp_pos.size();++j) {
			pos.push_back(orig_pos[j]);
		}
		*turn_idx += 1;
	}
	return status;
}




#endif
