#### COMPILATION OPTIONS ####


ifeq ($(shell hostname), uv100)
	GSL_FLAG 	= false
else
	GSL_FLAG        = true
endif

MACHINE		= -m64
OPT_FLAG	= -O3 -w
DBG_FLAG	= -O0 -g3

SOURCES_C	= nrutil.c nrcheck.c nrframe.c nrlinwww.c
SOURCES_CPP	= mathlib.cc naffutils.cc lsoc.cc t2ring.cc rdmfile.cc prtmfile.cc fft.cc ety.cc eigenv.cc pascalio.cc soltracy.cc tracy_lib.cc read_script.cc soleilcommon.cc max4_lib.cc nsls-ii_lib.cc physlib.cc lnlscommon.cc

#### DERIVED CONDITIONALS AND VARIABLES ####
ifeq ($(GSL_FLAG),true)
	GSL		= -lgsl -lgslcblas
	DFLAGS		= -DGLS
else
	GSL		= ~/bin/GSL/lib/libgsl.a ~/bin/GSL/lib/libgslcblas.a
	DFLAGS		= -DGLS
endif
ifeq ($(MAKECMDGOALS),tracyd)
	CFLAGS		= $(MACHINE) $(DBG_FLAG) $(DFLAGS)
else
	CFLAGS		= $(MACHINE) $(OPT_FLAG) $(DFLAGS)
endif

OBJECTS		= $(SOURCES_CPP:.cc=.o) $(SOURCES_C:.c=.o) 
LDFLAGS		= $(MACHINE)
LIBS		= libs/TPSA/libTPSALie$(MACHINE).a libs/nrecipes/nrecipes$(MACHINE).a libs/tracking_mp/tracking_mp$(MACHINE).a $(GSL) -lpthread -lgfortran


#### GENERATES DEPENDENCY FILE ####
$(shell g++ -MM $(SOURCES_CPP) $(SOURCES_C) > .depend)
-include .depend
ALLSVNFILES = $(shell find ./ | grep -v "\.svn" | grep -v ".[oa]")

#### TARGETS ####

all:	alllibs tracy


alllibs:
	cd libs/nrecipes; make all;
	cd libs/TPSA; make all;
	cd libs/tracking_mp; make all;

tracy: $(OBJECTS)
	g++ $(LDFLAGS) $(OBJECTS) $(LIBS) -o $@

tracyd:	$(OBJECTS)
	g++ $(LDFLAGS) $(OBJECTS) $(LIBS) -o $@

clean:
	rm -rf *.o tracy tracyd .depend *.out *.dat

cleanall: clean
	cd libs/nrecipes; make clean;
	cd libs/TPSA; make clean;
	cd libs/tracking_mp; make clean;
	cd tests/; make clean;

commit: cleanall
	svn add -q $(ALLSVNFILES)
	svn status
	svn commit
	


#### RULES ####

.c.o:
	gcc -c $(CFLAGS) $<

.cc.o:
	g++ -c $(CFLAGS) $<
