.DELETE_ON_ERROR:

hello.bin : say_hello.py cmdconsts.py
	python3 $< > $@

cmdconsts.py ltable.bin : lookup_table.py
	python3 $< > $@

.PHONY : flash
flash : hello.bin
	../flash.sh -w $<

.PHONY : flash-ltable
flash-ltable : ltable.bin
	../flash.sh -s -w $<
