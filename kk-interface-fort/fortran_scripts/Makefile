SRC = $(wildcard *.f90)
ifeq ($(OS),Windows_NT)
	FLAGS = --fcompiler=gnu95 --compiler=mingw32
	XX = f2py
else
	XX = f2py$(VER)
endif

methods: $(SRC)
	$(XX) -c $(FLAGS) -m $@ $^

clean:
	rm -rf *.o *.so __pycache__ *.pyc
