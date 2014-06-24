#include "flat_file.h"
#include "elements.h"
#include "auxiliary.h"
#include <fstream>

Status::type read_flat_file_tracy(const std::string& filename, std::vector<Element>& the_ring) {

	std::ifstream fp(filename);
	if (fp.fail()) return Status::file_not_found;

	int Fnum, Knum, idx, type, method;
	the_ring.clear();
	while (not fp.eof()) {

		Element e;

		// reads header
		fp >> e.fam_name >> Fnum >> Knum >> idx; if (fp.eof()) break;
		fp >> type >> method >> e.nr_steps;
		if (e.nr_steps < 1) e.nr_steps = 1;
		fp >> e.hmax >> e.hmax >> e.vmax >> e.vmax;

		// tracy starts with "begin" zero-length drift element...
		if (e.fam_name == "begin") {
			fp >> e.length;
			continue;
		}

		// element-type specifics
		switch (type) {
		case FlatFileType::marker:
			e.pass_method = PassMethod::pm_identity_pass;
			break;
		case FlatFileType::drift:
			e.pass_method = PassMethod::pm_drift_pass;
			fp >> e.length;
			break;
		case FlatFileType::corrector:
			e.pass_method = PassMethod::pm_corrector_pass;
			double tmpdbl; fp >> tmpdbl >> tmpdbl >> tmpdbl;
			int    tmpint; fp >> tmpint >> tmpint;
			fp >> tmpint >> e.hkick >> e.vkick;
			e.hkick = - e.hkick; // AT idiosyncrasies...
			break;
		case FlatFileType::cavity:
			e.pass_method = PassMethod::pm_cavity_pass;
			int hnumber; fp >> e.voltage >> e.frequency >> hnumber >> e.energy;
			e.voltage *= e.energy; e.frequency *= light_speed / (2*M_PI);
			break;
		case FlatFileType::mpole:
			double PdTPar, PdTerr;
			fp >> e.t_out[0] >> e.t_out[2] >> PdTPar >> PdTerr;
			fp >> e.length >> e.angle >> e.angle_in >> e.angle_out >> e.gap;
			e.angle *= e.length; e.angle_in *= M_PI/180.0; e.angle_out *= M_PI/180.0;
			if (e.angle != 0)
				e.pass_method = PassMethod::pm_bnd_mpole_symplectic4_pass;
			else
				e.pass_method = PassMethod::pm_str_mpole_symplectic4_pass;
			read_polynomials(fp, e);
			e.t_in[0] = -e.t_out[0]; e.t_in[2] = -e.t_out[2];
			double ang = M_PI*(PdTPar+PdTerr)/180.0;
			double C = cos(ang);
			double S = sin(ang);
			e.r_in [0*6+0] =  C; e.r_in [0*6+2] =  S;
			e.r_in [2*6+0] = -S; e.r_in [2*6+2] =  C;
			e.r_in [1*6+1] =  C; e.r_in [1*6+3] =  S;
			e.r_in [3*6+1] = -S; e.r_in [3*6+3] =  C;
			e.r_out[0*6+0] =  C; e.r_out[0*6+2] = -S;
			e.r_out[2*6+0] =  S; e.r_out[2*6+2] =  C;
			e.r_out[1*6+1] =  C; e.r_out[1*6+3] = -S;
			e.r_out[3*6+1] =  S; e.r_out[3*6+3] =  C;
		}


		the_ring.push_back(e); idx++;

	};

	return Status::success;

}

void read_polynomials(std::ifstream& fp, Element& e) {
	unsigned int nr_monomials, n_design, order;
	e.polynom_a = std::vector<double>(Element::default_polynom);
	e.polynom_b = std::vector<double>(Element::default_polynom);
	fp >> nr_monomials >> n_design;
	for(unsigned int i=0; i<nr_monomials; ++i) {
		fp >> order;
		if (order > e.polynom_b.size()) {
			e.polynom_a.resize(order,0);
			e.polynom_b.resize(order,0);
		}
		fp >> e.polynom_b[order-1] >> e.polynom_a[order-1];
	}
}
