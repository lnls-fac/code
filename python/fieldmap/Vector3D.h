#ifndef VECTOR3D_H
#define VECTOR3D_H

#include <ostream>

template <typename T = double>
class Vector3D {
public:
	Vector3D(const T& x_, const T& y_, const T& z_);
	T data[3];
	T& x,y,z;
};

template <typename T>
Vector3D<T>::Vector3D(const T& x_, const T& y_, const T& z_) :
	x(data[0]), y(data[1]), z(data[2])
{
	this->x = x_; this->y = y_; this->z = z_;
}

template <typename T>
std::ostream& operator<<(std::ostream& os, const Vector3D<T>& v)
{
  os << "(" << v.x << "," << v.y << "," << v.z << ")";
  return os;
}

#endif
