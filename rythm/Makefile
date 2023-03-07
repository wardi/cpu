.DELETE_ON_ERROR:

rythm.bin : rythm.py cmdconsts.py song.py cgram.py
	python3 $< > $@

cmdconsts.py ltable.bin : lookup_table.py
	python3 $< > $@

.PHONY : flash
flash : rythm.bin
	../flash.sh -w $<

.PHONY : flash-ltable
flash-ltable : ltable.bin
	../flash.sh -s -w $<
