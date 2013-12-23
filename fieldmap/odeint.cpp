#include <cmath>
#include <boost/numeric/odeint.hpp>
#include "API.h"

static const double electron_rest_energy = 0.00051099892811;  // [GeV]
static const double light_speed          = 299792458;         // [m/s]
static double       gamma_, beta_, brho_;
static const        FieldMap *fieldmap_;


static void set_field_map_and_energy(const FieldMap& fieldmap, const double& energy)
{
	gamma_ = energy / electron_rest_energy;
	beta_  = std::sqrt(1.0 - 1.0 / (gamma_ * gamma_));
	brho_  = 1e9 * (beta_ * energy / light_speed);
	fieldmap_ = &fieldmap;
}


void newton_lorentz_equation( const state_type &state , state_type &dstate_ds , const double s)
{
	// symbolic sugars
	const double &x         = state[0],     &y         = state[1],     &z         = state[2];
	const double &betax     = state[3],     &betay     = state[4],     &betaz     = state[5];
	double       &dx_ds     = dstate_ds[0], &dy_ds     = dstate_ds[1], &dz_ds     = dstate_ds[2];
	double       &dbetax_ds = dstate_ds[3], &dbetay_ds = dstate_ds[4], &dbetaz_ds = dstate_ds[5];

	Vector3D<double> r(x,y,z);
	Vector3D<double> b;
	try {
		b = fieldmap_->field(r);
	} catch (...) { }

	double alpha = 1 / brho_ / beta_;
	dx_ds     = betax;
	dy_ds     = betay;
	dz_ds     = betaz;
	dbetax_ds = - alpha * (betay * b.z - betaz * b.y);
	dbetay_ds = - alpha * (betaz * b.x - betax * b.z);
	dbetaz_ds = - alpha * (betax * b.y - betay * b.x);

}




struct push_back_state_and_time
{
    std::vector< state_type >& states_;
    std::vector< double >&     times_;

    push_back_state_and_time(std::vector<state_type> &states, std::vector< double > &times ) : states_(states), times_(times) { }

    void operator()(const state_type& state, double t)
    {
        states_.push_back(state);
        times_.push_back(t);
    }
};


void boost_integrate_const(
		const double& energy,
		const FieldMap& fieldmap,
		const double& si, const double& sf, size_t nr_pts, state_type& init_state,
		std::vector<double>& s, std::vector<state_type>& trajectory)
{
	//typedef boost::numeric::odeint::runge_kutta_cash_karp54< state_type > error_stepper_type;
	set_field_map_and_energy(fieldmap, energy);
	boost::numeric::odeint::runge_kutta4<state_type> stepper;
	push_back_state_and_time pb(trajectory,s);
	double ds = (sf-si)/(nr_pts-1.0);
	boost::numeric::odeint::integrate_const(stepper, newton_lorentz_equation, init_state, si, sf, ds, pb);

//	size_t steps = boost::numeric::odeint::integrate_adaptive(
//			boost::numeric::odeint::make_controlled<error_stepper_type>(1.0e-8, 1.0e-8),
//			newton_lorentz_equation,
//			init_state, 0.0, 1.0, 0.001, pb);
}
