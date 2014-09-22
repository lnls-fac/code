# TRACKING_MP
# ===========
# Author: 		Ximenes R. Resende
# email:  		xresende@gmail.com, ximenes.resende@lnls.br
# affiliation:	        LNLS - Laboratorio Nacional de Luz Sincrotron
# Date: 		2012-08-20

OBJECTS = $(addprefix $(OBJDIR)/, mp_task_mgr.o)
OBJDIR = build

.PHONY:	all tracking_mp

all:	tracking_mp

tracking_mp: $(OBJECTS)
	-rm $(OBJDIR)/tracking_mp.a
	ar r $(OBJDIR)/tracking_mp.a $(OBJDIR)/*.o 

$(OBJECTS): | $(OBJDIR)

$(OBJDIR):
	mkdir $(OBJDIR)

$(OBJDIR)/%.o: %.cc
	g++ -m64 -O2 -c $< -o $@

clean:
	rm -rf $(OBJDIR)
