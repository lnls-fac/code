#ifndef FIELDMAP_VECTOR3D_H
#define FIELDMAP_VECTOR3D_H

#include <ostream>

template <typename T = double>
class Vector3D {
public:
	Vector3D() : x(0), y(0), z(0) {}
	Vector3D(const T& x_, const T& y_, const T& z_) : x(x_), y(y_), z(z_) {}
	Vector3D(const Vector3D& v) : x(v.x), y(v.y), z(v.z) {}
	T x,y,z;
};

template <typename T>
std::ostream& operator<<(std::ostream& os, const Vector3D<T>& v)
{
  os << "(" << v.x << "," << v.y << "," << v.z << ")";
  return os;
}

#endif
