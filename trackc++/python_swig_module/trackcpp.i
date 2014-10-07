%module trackcpp

%{
#include "../elements.h"
#include "../kicktable.h"
#include "../auxiliary.h"
#include "../accelerator.h"
%}
%include "std_string.i"
%include "std_vector.i"
%include "stl.i"

namespace std {
    %template(trackcpp_StringVector) vector<string>;
    %template(trackcpp_DoubleVector) vector<double>;
    %template(trackcpp_ElementVector) vector<Element>;
}

%include "../elements.h"
%include "../kicktable.h"
%include "../auxiliary.h"
%include "../accelerator.h"
