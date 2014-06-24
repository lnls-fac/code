#include "commands.h"
#include <string>
#include <cmath>
#include <iostream>
#include <cstdlib>

std::string string_passmethods[] = {
		"pm_identity_pass",
		"pm_drift_pass",
		"pm_str_mpole_symplectic_pass",
		"pm_bnd_mpole_symplectic_pass",
		"pm_corrector_pass",
		"pm_cavity_pass",
		"pm_thinquad_pass",
		"pm_thinsext_pass",
		"pm_str_mpole_symplectic_pass",
		"pm_bnd_mpole_symplectic_pass",
};

std::string string_error_messages[] = {
		"success",
		"passmethod_not_defined",
		"passmethod_not_implemented",
		"particle_lost",
		"inconsistent_dimensions",
		"uninitialized_memory",
		"findorbit_not_converged",
		"findorbit_one_turn_matrix_problem",
		"file_not_found"
};

bool isfinite(const double& v) {
	return std::isfinite(v);
}

int main(int argc, char *argv[]) {
	if (argc == 1) {
		fprintf(stdout, "TRACKC++ [%s %s]\n", __DATE__, __TIME__);
		fprintf(stdout, "Accelerator Physics Group - LNLS\n");
		fprintf(stdout, "Campinas BRAZIL\n");
		fprintf(stdout, "contact: xresende@gmail.com\n");
		return EXIT_SUCCESS;
	};
	std::string cmd(argv[1]);
	if (cmd == "tests")    return cmd_tests(argc, argv);
	if (cmd == "dynap_xy") return cmd_dynap_xy(argc, argv);
	std::cerr << "trackc++: invalid command!" << std::endl;
	return EXIT_FAILURE;
}

