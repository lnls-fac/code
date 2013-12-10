#### COMPILATION OPTIONS ####
MACHINE		= -m64
OPT_FLAG	= -O3
DBG_FLAG	= -O0 -g3
DFLAGS          =
SOURCES_C       = 
SOURCES_CPP	= lattice.cpp elements.cpp passmethods.cpp trackc++.cpp

ifeq ($(MAKECMDGOALS),trackc++-debug)
	CFLAGS		= $(MACHINE) $(DBG_FLAG) $(DFLAGS)
else
	CFLAGS		= $(MACHINE) $(OPT_FLAG) $(DFLAGS)
endif

OBJECTS		= $(SOURCES_CPP:.cpp=.o) $(SOURCES_C:.c=.o) 
LDFLAGS		= $(MACHINE) 
LIBS		= tracking_mp/tracking_mp.a -lpthread


#### GENERATES DEPENDENCY FILE ####
$(shell g++ -MM $(SOURCES_CPP) $(SOURCES_C) > .depend)
-include .depend

#### TARGETS ####

all:	alllibs trackc++


alllibs:
	cd tracking_mp; make all;

trackc++: $(OBJECTS)
	g++ $(LDFLAGS) $(OBJECTS) $(LIBS) -o $@

trackc++-debug:	$(OBJECTS)
	g++ $(LDFLAGS) $(OBJECTS) $(LIBS) -o $@

clean:
	rm -rf *.o trackc++ trackc++-debug .depend *.out *.dat *~

cleanall: clean
	cd tracking_mp; make clean;


#### RULES ####

.c.o:
	gcc -c $(CFLAGS) $<

.cc.o:
	g++ -c $(CFLAGS) $<
.cpp.o:
	g++ -c $(CFLAGS) $<
