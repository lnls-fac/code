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
    %template(trackcpp_StringVector) vector<string>;
    %template(trackcpp_DoubleVector) vector<double>;
    %template(trackcpp_ElementVector) vector<Element>;
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
