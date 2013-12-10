# TRACKING_MP
# ===========
# Author: 		Ximenes R. Resende
# email:  		xresende@gmail.com, ximenes.resende@lnls.br
# affiliation:	LNLS - Laboratorio Nacional de Luz Sincrotron
# Date: 		2012-08-20

all:	tracking_mp

tracking_mp:
	rm -rf tracking_mp.a *.o
	g++ -m64 -O2 -c mp_task_mgr.cc
	#g++ -m64 -O2 -c fmap_mp.cc
	#g++ -m64 -O2 -c fmapdp_mp.cc
	ar r tracking_mp.a *.o 

clean:
	rm -rf *.o *.a *~

