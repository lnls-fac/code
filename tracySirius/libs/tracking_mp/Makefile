all:	tracking_mp-m64

tracking_mp-m32:
	rm -rf tracking_mp.a *.o
	g++ -m32 -O2 -c mp_task_mgr.cc
	g++ -m32 -O2 -c fmap_mp.cc
	g++ -m32 -O2 -c fmapdp_mp.cc
	g++ -m32 -O2 -c daxy_mp.cc
	g++ -m32 -O2 -c daex_mp.cc
	ar r tracking_mp-m32.a *.o 


tracking_mp-m64:
	rm -rf tracking_mp.a *.o
	g++ -m64 -O2 -c mp_task_mgr.cc
	g++ -m64 -O2 -c fmap_mp.cc
	g++ -m64 -O2 -c fmapdp_mp.cc
	g++ -m64 -O2 -c daxy_mp.cc
	g++ -m64 -O2 -c daex_mp.cc
	ar r tracking_mp-m64.a *.o 

tracking_mp-debug-m32:
	rm -rf tracking_mp.a *.o
	g++ -m32 -g3 -O0 -c mp_task_mgr.cc
	g++ -m32 -g3 -O0 -c fmap_mp.cc
	g++ -m32 -g3 -O0 -c fmapdp_mp.cc
	ar r tracking_mp-m32.a *.o 


tracking_mp-debug-m64:
	rm -rf tracking_mp.a *.o
	g++ -m64 -g3 -O0 -c mp_task_mgr.cc
	g++ -m64 -g3 -O0 -c fmap_mp.cc
	g++ -m64 -g3 -O0 -c fmapdp_mp.cc
	ar r tracking_mp-m64.a *.o 


clean:
	rm -rf *.o *.a

