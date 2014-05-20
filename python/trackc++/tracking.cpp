#include "trackc++.h"

// findm66
// -------
// returns a vector with 6-d transfer matrices, one for each element
//
// inputs:
//		line:	 		Element vector representing the beam transport line
//		closed_orbit:	Pos vector representing calculated closed orbit.
//
// outputs:
//		m66:			vector of (double*)-type elements. Each elements if a pointer
//						to a flat c array with 36 elements representing the transfer element of
//						that element. The matrix is is row-format: (drx_f/drx_i, drx_f/dpx_i, ..., dl_f/de_i, dl_f/dl_i)
//						===========
//						ATTENTION: !!! Memory for each matrix is supposed to be previously allocated !!!
//						===========
//		RETURN:			status do tracking (see 'auxiliary.h')


Status::type findm66 (const std::vector<Element>& line, const std::vector<Pos<double> >& closed_orbit, std::vector<double*> m66) {


	Status::type status  = Status::success;

	// checks consistency of data
	if (m66.size() != line.size()) {
		status = Status::inconsistent_dimensions;
		return status;
	}

	for(unsigned int i=0; i<line.size(); ++i) {

		std::vector<Pos<Tpsa<6,1> > > particle;
		particle.push_back(Tpsa<6,1>());
		particle[0].rx = Tpsa<6,1>(closed_orbit[i].rx, 0); particle[0].px = Tpsa<6,1>(closed_orbit[i].px, 1);
		particle[0].ry = Tpsa<6,1>(closed_orbit[i].ry, 2); particle[0].py = Tpsa<6,1>(closed_orbit[i].py, 3);
		particle[0].de = Tpsa<6,1>(closed_orbit[i].de, 4); particle[0].dl = Tpsa<6,1>(closed_orbit[i].dl, 5);

		// track through element
		if ((status = elementpass (line[i], particle)) != Status::success) return status;

		// minimum  check to see if memory of allocated for each transfer matrix
		if (m66[i] == NULL) {
			status = Status::uninitialized_memory;
			return status;
		}

		// RX
		*(m66[i] + 0*6+0) = particle[0].rx.c[1];*(m66[i] + 0*6+1) = particle[0].rx.c[2];
		*(m66[i] + 0*6+2) = particle[0].rx.c[3];*(m66[i] + 0*6+3) = particle[0].rx.c[4];
		*(m66[i] + 0*6+4) = particle[0].rx.c[5];*(m66[i] + 0*6+5) = particle[0].rx.c[6];
		// PX
		*(m66[i] + 1*6+0) = particle[0].px.c[1];*(m66[i] + 1*6+1) = particle[0].px.c[2];
		*(m66[i] + 1*6+2) = particle[0].px.c[3];*(m66[i] + 1*6+3) = particle[0].px.c[4];
		*(m66[i] + 1*6+4) = particle[0].px.c[5];*(m66[i] + 1*6+5) = particle[0].px.c[6];
		// RY
		*(m66[i] + 2*6+0) = particle[0].ry.c[1];*(m66[i] + 2*6+1) = particle[0].ry.c[2];
		*(m66[i] + 2*6+2) = particle[0].ry.c[3];*(m66[i] + 2*6+3) = particle[0].ry.c[4];
		*(m66[i] + 2*6+4) = particle[0].ry.c[5];*(m66[i] + 2*6+5) = particle[0].ry.c[6];
		// PY
		*(m66[i] + 3*6+0) = particle[0].py.c[1];*(m66[i] + 3*6+1) = particle[0].py.c[2];
		*(m66[i] + 3*6+2) = particle[0].py.c[3];*(m66[i] + 3*6+3) = particle[0].py.c[4];
		*(m66[i] + 3*6+4) = particle[0].py.c[5];*(m66[i] + 3*6+5) = particle[0].py.c[6];
		// DE
		*(m66[i] + 4*6+0) = particle[0].de.c[1];*(m66[i] + 4*6+1) = particle[0].de.c[2];
		*(m66[i] + 4*6+2) = particle[0].de.c[3];*(m66[i] + 4*6+3) = particle[0].de.c[4];
		*(m66[i] + 4*6+4) = particle[0].de.c[5];*(m66[i] + 4*6+5) = particle[0].de.c[6];
		// DL
		*(m66[i] + 5*6+0) = particle[0].dl.c[1];*(m66[i] + 5*6+1) = particle[0].dl.c[2];
		*(m66[i] + 5*6+2) = particle[0].dl.c[3];*(m66[i] + 5*6+3) = particle[0].dl.c[4];
		*(m66[i] + 5*6+4) = particle[0].dl.c[5];*(m66[i] + 5*6+5) = particle[0].dl.c[6];

	}

	return status;

}
