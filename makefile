CC = clang
CFLAGS = -std=c99 -Wall -c -pedantic
PY_PATH = /usr/include/python3.7m
LDFLAGS = -shared -lpython3.7m -lmol -dynamiclib -L/usr/lib/python3.7/config-3.7m-x86_64-linux-gnu -L../A4

all: swig libmol.so _molecule.so

swig: molecule.i
	swig3.0 -python molecule.i

_molecule.so: molecule_wrap.o
	$(CC) $(LDFLAGS) -o _molecule.so molecule_wrap.o -lm -Wl,-rpath=.

molecule_wrap.o: molecule_wrap.c
	$(CC) $(CFLAGS) molecule_wrap.c -fPIC -I$(PY_PATH) -o molecule_wrap.o

libmol.so: mol.o
	$(CC) -shared -o libmol.so mol.o -lm

mol.o: mol.c mol.h
	$(CC) $(CFLAGS) mol.c -fPIC -o mol.o

clean:
	rm *.o *.so