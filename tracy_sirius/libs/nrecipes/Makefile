all:	nrecipes-m64

nrecipes-m64:
	rm -rf nrecipes-m64.a
	gcc -c -O3 *.c
	ar r nrecipes-m64.a *.o
	rm -rf *.o

nrecipes-m32:
	rm -rf nrecipes-m32.a
	gcc -c -m32 -O3 *.c
	ar r nrecipes-m32.a *.o
	rm -rf *.o

clean:
	rm -rf *.o *.a
