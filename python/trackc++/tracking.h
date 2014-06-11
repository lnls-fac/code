#ifndef _TRACKING_H
#define _TRACKING_H

// TRACKC++
// ========
// Author: 		Ximenes R. Resende
// email:  		xresende@gmail.com, ximenes.resende@lnls.br
// affiliation:	LNLS - Laboratorio Nacional de Luz Sincrotron
// Date: 		Tue Dec 10 17:57:20 BRST 2013

#include "trackc++.h"


Status::type findm66 (const std::vector<Element>& line, const std::vector<Pos<double> >& closed_orbit, std::vector<double*> m66);


// linepass
// --------
// tracks particles along a beam transport line
//
// inputs:
//		line:	 		Element vector representing the beam transport line
//		orig_pos:		Pos vector representing initial positions of particles
//		element_offset:	equivalent to shifting the lattice so that '*element_offset' is the index for the first element
//		trajectory:		flag indicating that trajectory is to be recorded at entrance of all elements
//						(otherwise only the coordinates at the exit of last element is recorded)
// outputs:
//		pos:			Pos vector of particles' final coordinates (or trajetory)
//		element_offset:	in case of problems with passmethods, '*element_offset' is the index of the corresponding element
//		RETURN:			status do tracking (see 'auxiliary.h')

template <typename T>
Status::type elementpass (const Element& el, std::vector<Pos<T> >& orig_pos) {

	Status::type status = Status::success;

	switch (el.pass_method) {
	case PassMethod::pm_identity_pass:
		if ((status = pm_identity_pass<T>(orig_pos, el)) != Status::success) return status;
		break;
	case PassMethod::pm_drift_pass:
		if ((status = pm_drift_pass<T>(orig_pos, el)) != Status::success) return status;
		break;
	case PassMethod::pm_str_mpole_symplectic4_pass:
		if ((status = pm_str_mpole_symplectic4_pass<T>(orig_pos, el, false)) != Status::success) return status;
		break;
	case PassMethod::pm_str_mpole_symplectic4_rad_pass:
		if ((status = pm_str_mpole_symplectic4_pass<T>(orig_pos, el, true)) != Status::success) return status;
		break;
	case PassMethod::pm_bnd_mpole_symplectic4_pass:
		if ((status = pm_bnd_mpole_symplectic4_pass<T>(orig_pos, el, false)) != Status::success) return status;
		break;
	case PassMethod::pm_bnd_mpole_symplectic4_rad_pass:
		if ((status = pm_bnd_mpole_symplectic4_pass<T>(orig_pos, el, true)) != Status::success) return status;
		break;
	case PassMethod::pm_corrector_pass:
		if ((status = pm_corrector_pass<T>(orig_pos, el)) != Status::success) return status;
		break;
	case PassMethod::pm_cavity_pass:
		if ((status = pm_cavity_pass<T>(orig_pos, el)) != Status::success) return status;
		break;
	case PassMethod::pm_thinquad_pass:
		if ((status = pm_thinquad_pass<T>(orig_pos, el)) != Status::success) return status;
		break;
	case PassMethod::pm_thinsext_pass:
		if ((status = pm_thinsext_pass<T>(orig_pos, el)) != Status::success) return status;
		break;
	default:
		return Status::passmethod_not_defined;
	}

	return status;

}

template <typename T>
Status::type linepass (const std::vector<Element>& line, std::vector<Pos<T> >& orig_pos, std::vector<Pos<T> >& pos, int *element_offset, bool trajectory) {

	Status::type status = Status::success;

	int nr_elements  = line.size();
	int nr_particles = orig_pos.size();

	for(int i=0; i<nr_elements; ++i) {

		const int& e = *element_offset;    // syntactic-sugar for read-only access to element index
		const Element& element = line[e];  // syntactic-sugar for read-only access to element object parameters

		// stores trajectory at entrance of each element
		if (trajectory) {
			for(int j=0; j<nr_particles;++j) {
				pos.push_back(orig_pos[j]);
			}
		}

		switch (element.pass_method) {
			case PassMethod::pm_identity_pass:
				if ((status = pm_identity_pass<T>(orig_pos, element)) != Status::success) return status;
				break;
			case PassMethod::pm_drift_pass:
				if ((status = pm_drift_pass<T>(orig_pos, element)) != Status::success) return status;
				break;
			case PassMethod::pm_str_mpole_symplectic4_pass:
				if ((status = pm_str_mpole_symplectic4_pass<T>(orig_pos, element, false)) != Status::success) return status;
				break;
			case PassMethod::pm_str_mpole_symplectic4_rad_pass:
				if ((status = pm_str_mpole_symplectic4_pass<T>(orig_pos, element, true)) != Status::success) return status;
				break;
			case PassMethod::pm_bnd_mpole_symplectic4_pass:
				if ((status = pm_bnd_mpole_symplectic4_pass<T>(orig_pos, element, false)) != Status::success) return status;
				break;
			case PassMethod::pm_bnd_mpole_symplectic4_rad_pass:
				if ((status = pm_bnd_mpole_symplectic4_pass<T>(orig_pos, element, true)) != Status::success) return status;
				break;
			case PassMethod::pm_corrector_pass:
				if ((status = pm_corrector_pass<T>(orig_pos, element)) != Status::success) return status;
				break;
			case PassMethod::pm_cavity_pass:
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

		if (((orig_pos[0].rx < -1) or (orig_pos[0].rx > 1)) or ((orig_pos[0].ry < -1) or (orig_pos[0].ry > 1))) {
			std::cout << "kkk" << std::endl;
		}
		*element_offset = (*element_offset + 1) % nr_elements; // increment element index

	}

	// stores final particles' positions at the end of the line
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
//		element_offset:	equivalent to shifting the lattice so that '*element_offset' is the index for the first element
//		nr_turns:		number of turns for tracking
//
// outputs:
//		pos:			Pos vector of particles' coordinates of the turn_by_turn data (at end of the ring at each turn)
//		turn_idx:		in case of problems with passmethods, '*turn_idx' is the index of the corresponding turn
//		element_offset:	in case of problems with passmethods, '*element_offset' is the index of the corresponding element
//		RETURN:			status do tracking (see 'auxiliary.h')


template <typename T>
Status::type ringpass (const std::vector<Element>& ring, std::vector<Pos<T> >& orig_pos, std::vector<Pos<T> >& pos, const int nr_turns, int *turn_idx, int *element_offset) {

	Status::type status  = Status::success;

	*turn_idx = 0;
	for(int n=0; n<nr_turns; ++n) {
		std::vector<Pos<T> > tmp_pos;
		if ((status = linepass (ring, orig_pos, tmp_pos, element_offset, false)) != Status::success) return status;
		// records turn-by-turn data
		for(int j=0; j<tmp_pos.size();++j) {
			pos.push_back(orig_pos[j]);
		}
		*turn_idx += 1;
	}
	return status;
}


#endif
