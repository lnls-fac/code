#include <cmath>
#include <cstdlib>

#define idx(ix,iy) ((ix)*nx_+(iy))
#define f(ix,iy) (tabled_function_[(ix)*nx_+(iy)])


template <typename T>
class TabledFunction2D {


public:
	TabledFunction2D(const double& xmin, const double& xmax, const size_t nx,
					 const double& ymin, const double& ymax, const size_t ny,
					 const T* tabled_function);
	~TabledFunction2D() {
		delete [] tabled_function_dfdx_;
		delete [] tabled_function_dfdy_;
		delete [] tabled_function_d2fdxdy_;
		if (delete_tabled_function_) delete [] tabled_function_;
	}
	T interpolate(const double& x, const double& y) const;



private:

	size_t nx_;
	double xmin_, xmax_, dx_;
	size_t ny_;
	double ymin_, ymax_, dy_;
	const T* tabled_function_;
	bool delete_tabled_function_;
	T* tabled_function_dfdx_;
	T* tabled_function_dfdy_;
	T* tabled_function_d2fdxdy_;
	void calc_derivs();

};


template <typename T>
T TabledFunction2D<T>::interpolate(const double& x, const double& y) const
{
	// calcs indices and does range checking
	size_t ix1 = (size_t) std::floor(0.5 + (x - xmin_)/dx_);
	if ((ix1 < 0) or (ix1 > nx_)) {
		throw "interpolate: x is out of range";
	}
	size_t iy1 = (size_t) std::floor(0.5 + (y - ymin_)/dy_);
	if ((iy1 < 0) or (iy1 > ny_)) {
			throw "interpolate: y is out of range";
	}

	// calcs indices of 4 x-y counterclockwise bounding points
	size_t p1,p2,p3,p4;
	if (iy1 == ny_) {
		if (ix1 == nx_) {
			p1 = p2 = p3 = p4 = idx(iy1+0,ix1+0);
		} else {
			p1 = p4 = idx(iy1+0,ix1+0);
			p2 = p3 = idx(iy1+0,ix1+1);
		}
	} else {
		if (ix1 == nx_) {
			p1 = p2 = idx(iy1+0,ix1+0);
			p3 = p4 = idx(iy1+1,ix1+0);
		} else {
			// interior
			p1 = idx(iy1+0,ix1+0);
			p2 = idx(iy1+0,ix1+1);
			p3 = idx(iy1+1,ix1+1);
			p4 = idx(iy1+1,ix1+0);
		}
	}

	const T* f0  = this->tabled_function_;
	const T* fx  = this->tabled_function_dfdx_;
	const T* fy  = this->tabled_function_dfdy_;
	const T* fxy = this->tabled_function_d2fdxdy_;

	const T& x01 = f0[p1];
	const T& x02 = f0[p2];
	const T& x03 = f0[p3];
	const T& x04 = f0[p4];
	const T& x05 = fx[p1];
	const T& x06 = fx[p2];
	const T& x07 = fx[p3];
	const T& x08 = fx[p4];
	const T& x09 = fy[p1];
	const T& x10 = fy[p2];
	const T& x11 = fy[p3];
	const T& x12 = fy[p4];
	const T& x13 = fxy[p1];
	const T& x14 = fxy[p2];
	const T& x15 = fxy[p3];
	const T& x16 = fxy[p4];

	T a00 =  1*x01 + 0*x02 + 0*x03 + 0*x04 + 0*x05 + 0*x06 + 0*x07 + 0*x08 + 0*x09 + 0*x10 + 0*x11 + 0*x12 + 0*x13 + 0*x14 + 0*x15 + 0*x16;
	T a10 =  0*x01 + 0*x02 + 0*x03 + 0*x04 + 1*x05 + 0*x06 + 0*x07 + 0*x08 + 0*x09 + 0*x10 + 0*x11 + 0*x12 + 0*x13 + 0*x14 + 0*x15 + 0*x16;
	T a20 = -3*x01 + 3*x02 + 0*x03 + 0*x04 +-2*x05 +-1*x06 + 0*x07 + 0*x08 + 0*x09 + 0*x10 + 0*x11 + 0*x12 + 0*x13 + 0*x14 + 0*x15 + 0*x16;
	T a30 =  2*x01 +-2*x02 + 0*x03 + 0*x04 + 1*x05 + 1*x06 + 0*x07 + 0*x08 + 0*x09 + 0*x10 + 0*x11 + 0*x12 + 0*x13 + 0*x14 + 0*x15 + 0*x16;
	T a01 =  0*x01 + 0*x02 + 0*x03 + 0*x04 + 0*x05 + 0*x06 + 0*x07 + 0*x08 + 1*x09 + 0*x10 + 0*x11 + 0*x12 + 0*x13 + 0*x14 + 0*x15 + 0*x16;
	T a11 =  0*x01 + 0*x02 + 0*x03 + 0*x04 + 0*x05 + 0*x06 + 0*x07 + 0*x08 + 0*x09 + 0*x10 + 0*x11 + 0*x12 + 1*x13 + 0*x14 + 0*x15 + 0*x16;
	T a21 =  0*x01 + 0*x02 + 0*x03 + 0*x04 + 0*x05 + 0*x06 + 0*x07 + 0*x08 +-3*x09 + 3*x10 + 0*x11 + 0*x12 +-2*x13 +-1*x14 + 0*x15 + 0*x16;
	T a31 =  0*x01 + 0*x02 + 0*x03 + 0*x04 + 0*x05 + 0*x06 + 0*x07 + 0*x08 + 2*x09 +-2*x10 + 0*x11 + 0*x12 + 1*x13 + 1*x14 + 0*x15 + 0*x16;
	T a02 = -3*x01 + 0*x02 + 3*x03 + 0*x04 + 0*x05 + 0*x06 + 0*x07 + 0*x08 +-2*x09 + 0*x10 +-1*x11 + 0*x12 + 0*x13 + 0*x14 + 0*x15 + 0*x16;
	T a12 =  0*x01 + 0*x02 + 0*x03 + 0*x04 +-3*x05 + 0*x06 + 3*x07 + 0*x08 + 0*x09 + 0*x10 + 0*x11 + 0*x12 +-2*x13 + 0*x14 +-1*x15 + 0*x16;
	T a22 =  9*x01 +-9*x02 +-9*x03 + 9*x04 + 6*x05 + 3*x06 +-6*x07 +-3*x08 + 6*x09 +-6*x10 + 3*x11 +-3*x12 + 4*x13 + 2*x14 + 2*x15 + 1*x16;
	T a32 = -6*x01 + 6*x02 + 6*x03 +-6*x04 +-3*x05 +-3*x06 + 3*x07 + 3*x08 +-4*x09 + 4*x10 +-2*x11 + 2*x12 +-2*x13 +-2*x14 +-1*x15 +-1*x16;
	T a03 =  2*x01 + 0*x02 +-2*x03 + 0*x04 + 0*x05 + 0*x06 + 0*x07 + 0*x08 + 1*x09 + 0*x10 + 1*x11 + 0*x12 + 0*x13 + 0*x14 + 0*x15 + 0*x16;
	T a13 =  0*x01 + 0*x02 + 0*x03 + 0*x04 + 2*x05 + 0*x06 +-2*x07 + 0*x08 + 0*x09 + 0*x10 + 0*x11 + 0*x12 + 1*x13 + 0*x14 + 1*x15 + 0*x16;
	T a23 = -6*x01 + 6*x02 + 6*x03 +-6*x04 +-4*x05 +-2*x06 + 4*x07 + 2*x08 +-3*x09 + 3*x10 +-3*x11 + 3*x12 +-2*x13 +-1*x14 +-2*x15 +-1*x16;
	T a33 =  4*x01 +-4*x02 +-4*x03 + 4*x04 + 2*x05 + 2*x06 +-2*x07 +-2*x08 + 2*x09 +-2*x10 + 2*x11 +-2*x12 + 1*x13 + 1*x14 + 1*x15 + 1*x16;


	double X = (x - (xmin_ + ix1 * dx_))/dx_;
	double Y = (y - (ymin_ + iy1 * dy_))/dy_;

	T   r = a00 +
			a10 * (X) + a20 * (X*X) + a30 * (X*X*X) +
			a01 * (Y) + a11 * (X*Y) + a21 * (X*X*Y) + a31 * (X*X*X*Y) +
			a02 * (Y*Y) + a12 * (X*Y*Y) + a22 * (X*X*Y*Y) + a32 * (X*X*X*Y*Y) +
			a03 * (Y*Y*Y) + a13 * (X*Y*Y*Y) + a23 * (X*X*Y*Y*Y) + a33 * (X*X*X*Y*Y*Y);

	return r;

}

template <typename T>
void TabledFunction2D<T>::calc_derivs()
{
	// only interior: at boundaries, using zero derivatives.
	for(size_t iy=1; iy<ny_-1; ++iy) {
		for(size_t ix=1; ix<nx_-1; ++ix) {
			tabled_function_dfdx_   [idx(iy,ix)] = (f(iy,ix+1) - f(iy,ix-1))/(2*dx_);
			tabled_function_dfdy_   [idx(iy,ix)] = (f(iy+1,ix) - f(iy-1,ix))/(2*dy_);
			tabled_function_d2fdxdy_[idx(iy,ix)] = (f(iy+1,ix+1) - f(iy+1,ix-1) - f(iy-1,ix+1) + f(iy-1,ix-1)) / (4 * dx_ * dy_);
		}
	}
}

template <typename T>
TabledFunction2D<T>::TabledFunction2D(
		const double& xmin, const double& xmax, const size_t nx,
		const double& ymin, const double& ymax, const size_t ny,
		const T* tabled_function) :
		nx_(nx), xmin_(xmin), xmax_(xmax),
		ny_(ny), ymin_(ymin), ymax_(ymax),
		tabled_function_(tabled_function),
		delete_tabled_function_(false)
{
	dx_ = (xmax_ - xmin_)/(nx_ - 1);
	dy_ = (ymax_ - ymin_)/(ny_ - 1);
	tabled_function_dfdx_    = new T [nx_ * ny_]();
	tabled_function_dfdy_    = new T [nx_ * ny_]();
	tabled_function_d2fdxdy_ = new T [nx_ * ny_]();
	calc_derivs();
}


#undef f
#undef idx
