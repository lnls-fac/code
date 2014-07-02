# TRACKC++
# ========
# Author: 		Ximenes R. Resende
# email:  		xresende@gmail.com, ximenes.resende@lnls.br
# affiliation:	LNLS - Laboratorio Nacional de Luz Sincrotron
# Date: 		Tue Dec 10 17:57:20 BRST 2013


#### COMPILATION OPTIONS ####
CC		= gcc
CXX		= g++
MACHINE		= -m64
OPT_FLAG	= -O2 -std=c++11
DBG_FLAG	= -O0 -g3 -std=c++11 
DFLAGS          =
SOURCES_C       = 
SOURCES_CPP	= lattice.cpp elements.cpp passmethods.cpp tracking.cpp trackc++.cpp tests.cpp sirius_v500.cpp flat_file.cpp optics.cpp dynap.cpp commands.cpp output.cpp
LIBS            = tracking_mp/tracking_mp.a -lpthread -lgsl -lgslcblas
INC             = 

ifeq ($(MAKECMDGOALS),trackc++-debug)
	CFLAGS		= $(MACHINE) $(DBG_FLAG) $(DFLAGS)
else
	CFLAGS		= $(MACHINE) $(OPT_FLAG) $(DFLAGS)
endif

OBJECTS		= $(SOURCES_CPP:.cpp=.o) $(SOURCES_C:.c=.o) 
LDFLAGS		= $(MACHINE) 


#### DERIVED CONDITIONALS AND VARIABLES ####
ifeq ($(shell hostname), uv100)
    CC          = /progs/users/gcc-4.7.3/bin/gcc
    CXX         = /progs/users/gcc-4.7.3/bin/g++
    LIBS        = -Wl,-rpath,/progs/users/gcc-4.7.3/lib64 tracking_mp/tracking_mp.a -lpthread ~/bin/GSL/lib/libgsl.a ~/bin/GSL/lib/libgslcblas.a
    INC         = -I../bin/GSL/include/
endif

#### GENERATES DEPENDENCY FILE ####
$(shell $(CXX) -MM $(SOURCES_CPP) $(SOURCES_C) > .depend)
-include .depend

#### TARGETS ####

all:	alllibs trackc++


alllibs:
	cd tracking_mp; make all;

trackc++: $(OBJECTS)
	$(CXX) $(LDFLAGS) $(OBJECTS) $(LIBS) -o $@

trackc++-debug:	$(OBJECTS)
	$(CXX) $(LDFLAGS) $(OBJECTS) $(LIBS) -o $@

clean:
	rm -rf *.o trackc++ trackc++-debug .depend *.out *.dat *~

cleanall: clean
	cd tracking_mp; make clean;


#### RULES ####

.c.o:
	$(CC) -c $(CFLAGS) $(INC) $<

.cc.o:
	$(CXX) -c $(CFLAGS) $(INC) $<
.cpp.o:
	$(CXX) -c $(CFLAGS) $(INC) $<
