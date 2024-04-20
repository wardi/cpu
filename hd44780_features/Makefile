.DELETE_ON_ERROR:

prog.bin ltable.bin : features.py
	./features.py -p prog.bin -l ltable.bin

.PHONY : flash
flash : prog.bin
	../flash.sh -s -w $<

.PHONY : flash-ltable
flash-ltable : ltable.bin
	../flash.sh -s -w $<
