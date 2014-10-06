
#### COMPILATION OPTIONS ####
CC		= gcc
CXX		= g++
MACHINE		= -m64
OPT_FLAG	= -O3 -std=c++11
DBG_FLAG	= -O0 -g3 -std=c++11 
DFLAGS          =
SOURCES_I = trackcpp.i
SOURCES_C       = 
SOURCES_CPP	= 	lattice.cpp \
			elements.cpp \
			passmethods.cpp \
			tracking.cpp \
			trackc++.cpp \
			tests.cpp \
			sirius_v500.cpp \
			flat_file.cpp optics.cpp \
			dynap.cpp commands.cpp \
			output.cpp \
			kicktable.cpp

LIBS            = tracking_mp/build/tracking_mp.a -lpthread -lgsl -lgslcblas
INC             = 

all: _trackcpp.so

_trackcpp.so: trackcpp_wrap.o
	g++ -shared trackcpp_wrap.o elements.o kicktable.o trackc++.o -o _trackcpp.so

trackcpp_wrap.o: trackcpp_wrap.cxx
	g++ --std=c++11 -c trackcpp_wrap.cxx ../elements.cpp ../kicktable.cpp ../trackc++.cpp -I/usr/include/python3.4 -I../ -fPIC

trackcpp_wrap.cxx: trackcpp.i
	swig -c++ -python trackcpp.i

clean:
	-rm -rf *.o *.so *_wrap.cxx __pycache__ trackcpp.py
