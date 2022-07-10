video.bin : video.py nmconsts.py
	python video.py

video.py : video.enc.gz encoder.py
	python encoder.py $< > $@

video.enc.gz : no-moon-test.mov extract.py
	python extract.py $< $@

mnconsts.py : lookup_table.py
	python lookup_table.py > $@

.PHONY : flash
flash : video.bin
	../flash.sh -w video.bin
