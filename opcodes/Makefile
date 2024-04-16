.DELETE_ON_ERROR:

prog.bin ltable.bin : opcodes.py
	python3 opcodes.py -p prog.bin -l ltable.bin

.PHONY : flash
flash : prog.bin
	../flash.sh -s -w $<

.PHONY : flash-ltable
flash-ltable : ltable.bin
	../flash.sh -s -w $<
