#include "trackc++.h"
#include <ctime>
#include <cstdlib>
#include <string>

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
		"file_not_found",
		"file_not_opened"
};

std::string string_version = "TRACKC++ version(" + std::string(__DATE__) + " " + std::string(__TIME__) + ")";

bool verbose_on = true;

bool isfinite(const double& v) {
	return std::isfinite(v);
}

int main(int argc, char *argv[]) {
	if (argc == 1) {
		print_header (stdout);
		return EXIT_SUCCESS;
	};
	std::string cmd(argv[1]);
	if (cmd == "tests")    return cmd_tests(argc, argv);
	if (cmd == "dynap_xy") return cmd_dynap_xy(argc, argv);
	if (cmd == "dynap_ex") return cmd_dynap_ex(argc, argv);
	std::cerr << "trackc++: invalid command!" << std::endl;
	return EXIT_FAILURE;
}

std::string get_timestamp() {

	char buffer[30];
	time_t t = time(NULL);   // get time now
	struct tm* now = localtime(&t);
	sprintf(buffer, "[%04i-%02i-%02i %02i:%02i:%02i]", 1900+now->tm_year, 1+now->tm_mon, now->tm_mday, now->tm_hour, now->tm_min, now->tm_sec);
	return std::string(buffer);
}
