.DELETE_ON_ERROR:

prog.bin : maze.py cmdconsts.py cgram.py map.txt
	python3 $< $@

cmdconsts.py ltable.bin : lookup_table.py
	python3 $< > $@

map.txt : genmaze.py maze_template2.png
	python3 $< maze_template2.png 42069 $@

.PHONY : flash
flash : prog.bin
	../flash.sh -w $<

.PHONY : flash-ltable
flash-ltable : ltable.bin
	../flash.sh -s -w $<
