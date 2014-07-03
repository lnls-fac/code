#include "lattice.h"
#include "output.h"
#include "accelerator.h"
#include "elements.h"
#include <vector>
#include <cstdlib>


Status::type print_closed_orbit(const Accelerator& accelerator, const std::vector<Pos<double>>& cod, const std::string& filename) {

	FILE* fp;
	fp = fopen(filename.c_str(), "w");
	if (fp == nullptr) return Status::file_not_opened;

	const std::vector<Element>& the_ring = accelerator.lattice;

	const char str[] = "----------------------";

	print_header(fp);
	fprintf(fp, "# [closed-orbit]\n");
	fprintf(fp, "# ebeam_energy[eV] : %f\n", accelerator.energy);
	fprintf(fp, "# harmonic_number  : %i\n", accelerator.harmonic_number);
	fprintf(fp, "# cavity_state     : %s\n", accelerator.cavity_on ? "on" : "off");
	fprintf(fp, "# radiation_state  : %s\n", accelerator.radiation_on ? "on" : "off");
	fprintf(fp, "# chamber_state    : %s\n", accelerator.vchamber_on ? "on" : "off");
	fprintf(fp, "\n");
	fprintf(fp, "%-5s %-15s %-22s %-22s %-22s %-22s %-22s %-22s %-22s\n", "# idx", "fam_name", "s[m]", "rx[m]", "ry[m]", "de", "px[rad]", "py[rad]", "dl[m]");
	fprintf(fp, "%-5s %-15s %-22s %-22s %-22s %-22s %-22s %-22s %-22s\n", "# ---", "---------------", str, str, str, str, str, str, str);

	double s = 0;
	for(unsigned int i=0; i<the_ring.size(); ++i) {
		fprintf(fp, "%05i %-15s %+22.15E %+22.15E %+22.15E %+22.15E %+22.15E %+22.15E %+22.15E\n", i+1, the_ring[i].fam_name.c_str(), s, cod[i].rx, cod[i].ry, cod[i].de, cod[i].px, cod[i].py, cod[i].dl);
		s += the_ring[i].length;
	}
	fclose(fp);
	return Status::success;
}

Status::type print_dynapgrid(const Accelerator& accelerator, const std::vector<DynApGridPoint>& grid, const std::string& label, const std::string& filename) {

	FILE* fp;
	fp = fopen(filename.c_str(), "w");
	if (fp == nullptr) return Status::file_not_opened;

	const char str[] = "----------------------";

	print_header(fp);
	fprintf(fp, "# %s\n", label.c_str());
	fprintf(fp, "# ebeam_energy[eV]  : %f\n", accelerator.energy);
	fprintf(fp, "# harmonic_number   : %i\n", accelerator.harmonic_number);
	fprintf(fp, "# cavity_state      : %s\n", accelerator.cavity_on ? "on" : "off");
	fprintf(fp, "# radiation_state   : %s\n", accelerator.radiation_on ? "on" : "off");
	fprintf(fp, "# chamber_state     : %s\n", accelerator.vchamber_on ? "on" : "off");
	fprintf(fp, "\n");
	fprintf(fp, "%-5s %-5s %-5s %-5s %-22s %-22s %-22s %-22s %-22s %-22s %-22s\n",  "# s_e", "l_t", "l_e", "l_p", "start_s[m]", "rx[m]", "ry[m]", "de", "px[rad]", "py[rad]", "dl[m]");
	fprintf(fp, "%-5s %-5s %-5s %-5s %-22s %-22s %-22s %-22s %-22s %-22s %-22s\n",  "# ---", "-----", "-----", "-----", str, str, str, str, str, str, str);

	std::vector<double> s = latt_findspos(accelerator.lattice, latt_range(accelerator.lattice));
	for(unsigned int i=0; i<grid.size(); ++i) {
		const Pos<double>& p = grid[i].p;
		fprintf(fp, "%-5i %-5i %-5i %-5i %+22.15E %+22.15E %+22.15E %+22.15E %+22.15E %+22.15E %+22.15E\n",  grid[i].start_element, grid[i].lost_turn, grid[i].lost_element, grid[i].lost_plane, s[grid[i].start_element], p.rx, p.ry, p.de, p.px, p.py, p.dl);
	}
	fclose(fp);
	return Status::success;
}

void print_header (FILE* fp) {
	fprintf(fp, "# %s\n", string_version.c_str());
	fprintf(fp, "# Accelerator Physics Group - LNLS\n");
	fprintf(fp, "# Campinas BRAZIL\n");
	fprintf(fp, "# contact: xresende@gmail.com\n");
}
