# TRACKING_MP
# ===========
# Author: 		Ximenes R. Resende
# email:  		xresende@gmail.com, ximenes.resende@lnls.br
# affiliation:	LNLS - Laboratorio Nacional de Luz Sincrotron
# Date: 		2012-08-20

OBJECTS = $(addprefix $(OBJDIR)/, mp_task_mgr.o)
OBJDIR = build

all:	tracking_mp

tracking_mp: $(OBJECTS)
	#rm -rf tracking_mp.a $(OBJDIR)/*.o
	#g++ -m64 -O2 -c mp_task_mgr.cc -o $(OBJDIR)/mp_task_mgr.o
	#g++ -m64 -O2 -c fmap_mp.cc
	#g++ -m64 -O2 -c fmapdp_mp.cc
	-rm $(OBJDIR)/tracking_mp.a
	ar r $(OBJDIR)/tracking_mp.a $(OBJDIR)/*.o 

$(OBJECTS): | $(OBJDIR)

$(OBJDIR):
	mkdir $(OBJDIR)

$(OBJDIR)/%.o: %.cc
	g++ -m64 -O2 -c $< -o $@

clean:
	rm -rf $(OBJDIR)
