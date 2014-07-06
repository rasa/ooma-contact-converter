CSVS=$(wildcard *.csv)

TXTS=$(CSVS:.csv=.ooma.txt)

%.ooma.txt: %.csv
	rm -f "$<.tmp"
	iconv -f UTF-16 -t UTF-8  "$<" >"$<.tmp"
	python google-contacts-to-ooma.py "$<.tmp" "$@"
	rm -f "$<.tmp"

.PHONY: all
all:	$(TXTS)

clean:
	rm -f $(TXTS)
