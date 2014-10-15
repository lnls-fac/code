
#include "elementswrapper.h"


Element marker_wrapper(const std::string &fam_name_) {
    return Element::marker(fam_name_);
}

Element bpm_wrapper(const std::string &fam_name_) {
    return Element::bpm(fam_name_);
}

Element hcorrector_wrapper(const std::string &fam_name_, const double &length_, const double &hkick_) {
    return Element::hcorrector(fam_name_, length_, hkick_);
}

Element vcorrector_wrapper(const std::string &fam_name_, const double &length_, const double &vkick_) {
    return Element::vcorrector(fam_name_, length_, vkick_);
}

Element corrector_wrapper(const std::string &fam_name_, const double &length_, const double &hkick_, const double &vkick_) {
    return Element::corrector(fam_name_, length_, hkick_, vkick_);
}

Element drift_wrapper(const std::string &fam_name_, const double &length_) {
    return Element::drift(fam_name_, length_);
}

Element rbend_wrapper(const std::string &fam_name_, const double &length_, const double &angle_, const double &angle_in_, const double &angle_out_, const double &K_, const double &S_) {
    return Element::rbend(fam_name_, length_, angle_, angle_in_, angle_out_, K_, S_);
}

Element quadrupole_wrapper(const std::string &fam_name_, const double &length_, const double &K_, const int nr_steps_) {
    return Element::quadrupole(fam_name_, length_, K_, nr_steps_);
}

Element sextupole_wrapper(const std::string &fam_name_, const double &length_, const double &S_, const int nr_steps_) {
    return Element::sextupole(fam_name_, length_, S_, nr_steps_);
}

Element rfcavity_wrapper(const std::string &fam_name_, const double &length_, const double &frequency_, const double &voltage_) {
    return Element::rfcavity(fam_name_, length_, frequency_, voltage_);
}
