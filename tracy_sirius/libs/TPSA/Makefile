all:	tpsa-m64

tpsa-m64:
	rm -rf libTPSALie-m64.a
	gfortran -c -g -O3 -Wall -fbounds-check -fPIC LieLib.f TPSALib.f
	ar r libTPSALie-m64.a *.o
	rm -rf *.o

tpsa-m32:
	rm -rf libTPSALie-m32.a
	gfortran -c -g -m32 -O3 -Wall -fbounds-check -fPIC LieLib.f TPSALib.f
	ar r libTPSALie-m32.a *.o
	rm -rf *.o

clean:
	rm -rf *.o *.a
