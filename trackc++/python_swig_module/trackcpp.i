%module trackcpp

%{
#include "../elements.h"
#include "../kicktable.h"
#include "../auxiliary.h"
#include "../accelerator.h"
%}
%include "carrays.i"
%include "std_string.i"
%include "std_vector.i"
%include "stl.i"

namespace std {
    %template(cppStringVector) vector<string>;
    %template(cppDoubleVector) vector<double>;
    %template(cppElementVector) vector<Element>;
}

%inline %{
double c_array_get(double* v, int i) {
    return v[i];
}
void c_array_set(double* v, int i, double x) {
    v[i] = x;
}
%}

%include "../elements.h"
%include "../kicktable.h"
%include "../auxiliary.h"
%include "../accelerator.h"
