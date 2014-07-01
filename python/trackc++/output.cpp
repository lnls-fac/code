#include "lattice.h"
#include "output.h"
#include "accelerator.h"
#include "elements.h"
#include <vector>
#include <cstdlib>


Status::type print_closed_orbit(const Accelerator& accelerator, const std::vector<Pos<double>>& cod, const std::string& filename) {
	FILE* fp;
	fp = fopen(filename.c_str(), "w");
	if (fp == NULL) return Status::file_not_opened;

	const std::vector<Element>& the_ring = accelerator.lattice;

	print_header(fp);
	fprintf(fp, "# [closed-orbit]\n");
	fprintf(fp, "# ebeam_energy[eV] : %f\n", accelerator.energy);
	fprintf(fp, "# harmonic_number  : %i\n", accelerator.harmonic_number);
	fprintf(fp, "# cavity_state     : %s\n", accelerator.cavity_on ? "on" : "off");
	fprintf(fp, "# radiation_state  : %s\n", accelerator.radiation_on ? "on" : "off");
	fprintf(fp, "# chamber_state    : %s\n", accelerator.vchamber_on ? "on" : "off");
	fprintf(fp, "\n");
	fprintf(fp, "%-5s %-15s %-23s %-23s %-23s %-23s %-23s %-23s %-23s\n", "# idx", "fam_name", "s[m]", "rx[m]", "px[rad]", "ry[m]", "py[rad]", "de", "dl[m]");
	fprintf(fp, "%-5s %-15s %-23s %-23s %-23s %-23s %-23s %-23s %-23s\n", "# ---", "---------------", "-----------------------", "-----------------------", "-----------------------", "-----------------------", "-----------------------", "-----------------------", "-----------------------");
	double s = 0;
	for(unsigned int i=0; i<the_ring.size(); ++i) {
		fprintf(fp, "%05i %-15s %+23.16E %+23.16E %+23.16E %+23.16E %+23.16E %+23.16E %+23.16E\n", i+1, the_ring[i].fam_name.c_str(), s, cod[i].rx, cod[i].px, cod[i].ry, cod[i].py, cod[i].de, cod[i].dl);
		s += the_ring[i].length;
	}
	fclose(fp);
	return Status::success;
}

Status::type print_dynapgrid(const Accelerator& accelerator, const std::vector<DynApGridPoint>& grid, const std::string& label, const std::string& filename) {
	FILE* fp;
	fp = fopen(filename.c_str(), "w");
	if (fp == NULL) return Status::file_not_opened;
	print_header(fp);
	fprintf(fp, "# %s\n", label.c_str());
	fprintf(fp, "# ebeam_energy[eV]  : %f\n", accelerator.energy);
	fprintf(fp, "# harmonic_number   : %i\n", accelerator.harmonic_number);
	fprintf(fp, "# cavity_state      : %s\n", accelerator.cavity_on ? "on" : "off");
	fprintf(fp, "# radiation_state   : %s\n", accelerator.radiation_on ? "on" : "off");
	fprintf(fp, "# chamber_state     : %s\n", accelerator.vchamber_on ? "on" : "off");
	fprintf(fp, "\n");
	fprintf(fp, "%-15s %-23s %-23s %-23s %-23s %-23s %-23s %-23s %-12s %-9s %-10s\n",  "# start_element", "start_s[m]", "rx[m]", "px[rad]", "ry[m]", "py[rad]", "de", "dl[m]", "lost_element", "lost_turn", "lost_plane");
	fprintf(fp, "%-15s %-23s %-23s %-23s %-23s %-23s %-23s %-23s %-12s %-9s %-10s\n",  "# -------------", "-----------------------", "-----------------------", "-----------------------", "-----------------------", "-----------------------", "-----------------------", "-----------------------", "------------", "---------", "----------");

	std::vector<double> s = latt_findspos(accelerator.lattice, latt_range(accelerator.lattice));
	for(unsigned int i=0; i<grid.size(); ++i) {
		const Pos<double>& p = grid[i].p;
		fprintf(fp, "%-15i %+23.16E %+23.16E %+23.16E %+23.16E %+23.16E %+23.16E %+23.16E %-12i %-9i %-10i\n",  grid[i].start_element, s[grid[i].start_element], p.rx, p.px, p.ry, p.py, p.de, p.dl, grid[i].lost_element, grid[i].lost_turn, grid[i].lost_plane);
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
