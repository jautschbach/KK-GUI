VER = 
all:
	@echo "Compiling methods..."
	cd fortran_scripts;make VER=$(VER)
	@echo "Succesfully built methods module for python "$(VER)

clean:
	@echo "Changing into fortran_scripts directory. Executing clean..."
	cd fortran_scripts;make clean
	@echo "Changing into scripts directory. Executing clean..."
	cd scripts;make clean
