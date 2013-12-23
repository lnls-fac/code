#include <boost/numeric/odeint.hpp>

/* The type of container used to hold the state vector */
typedef std::vector< double > state_type;

const double gam = 0.15;


/* The rhs of x' = f(x) defined as a class */
class harm_osc {

    double m_gam;

public:
    harm_osc( double gam ) : m_gam(gam) { }

    void operator() ( const state_type &x , state_type &dxdt , const double /* t */ )
    {
        dxdt[0] = x[1];
        dxdt[1] = -x[0] - m_gam*x[1];
        dxdt[2] = x[3];
        dxdt[3] = -x[2] - m_gam*x[3];
    }
};

struct push_back_state_and_time
{
    std::vector< state_type >& m_states;
    std::vector< double >& m_times;

    push_back_state_and_time( std::vector< state_type > &states , std::vector< double > &times )
    : m_states( states ) , m_times( times ) { }

    void operator()( const state_type &x , double t )
    {
        m_states.push_back( x );
        m_times.push_back( t );
        std::cout << t << " " << x[0] << std::endl;
    }
};



void test() {

	std::vector<state_type> x_vec;
	std::vector<double> t_vec;
	std::vector<double> x(4);
	x[0] = 1.0;
	x[1] = 0.0;
	x[2] = 1.0;
	x[3] = 0.0;

	harm_osc go(gam);

	boost::numeric::odeint::runge_kutta4< state_type > stepper;

	boost::numeric::odeint::integrate_const(
			stepper,
			go,
			x,
			0.0, 20.0, 0.01,
			push_back_state_and_time(x_vec,t_vec)
	);



}
