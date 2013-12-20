#ifndef VECTOR3D_H
#define VECTOR3D_H

template <typename T = double>
class Vector3D {
public:
	Vector3D(const T& x_ = 0, const T& y_ = 0, const T& z_ = 0);
	T data[3];
	T& x,y,z;
};

template <typename T>
Vector3D<T>::Vector3D(const T& x_, const T& y_, const T& z_) :
	x(data[0]), y(data[1]), z(data[2])
{
	this->x = x_; this->y = y_; this->z = z_;
}

#endif
