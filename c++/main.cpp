#include <iostream>

#include "TabledFunction2D.h"

void test_bicubic_interpolation() {

	size_t nx = 21;
	size_t ny = 11;
	double ymin = -10, ymax = 10;
	double xmin = -30, xmax = 30;
	double *f = new double [nx*ny];
	for(size_t i=0; i<ny; ++i) {
		double y = ymin + i * (ymax - ymin) / (ny - 1);
		for(size_t j=0; j<nx; ++j) {
			double x = xmin + j * (xmax - xmin) / (nx - 1);
			f[i*nx+j] =  1 + 2 * x + 3 * y + 4 * x * y;
		}
	}

	TabledFunction2D<double> tf(xmin,xmax,nx,ymin,ymax,ny,f);

	size_t iy = 5;
	size_t ix = 7;
	double y = ymin + iy * (ymax - ymin) / (ny - 1);
	double x = xmin + ix * (xmax - xmin) / (nx - 1);
	double fb = tf.interpolate(x,y);
	double ff = f[iy*nx+ix];
	std::cout << ff << " -> " << fb << std::endl;


}


int main() {

	//test_trajectory();
	test_bicubic_interpolation();

}
