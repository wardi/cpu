.DELETE_ON_ERROR:

prog.bin : maze.py cmdconsts.py genmaze.py cgram.py
	python3 $< $@

cmdconsts.py ltable.bin : lookup_table.py
	python3 $< > $@

.PHONY : flash
flash : prog.bin
	../flash.sh -w $<

.PHONY : flash-ltable
flash-ltable : ltable.bin
	../flash.sh -s -w $<
