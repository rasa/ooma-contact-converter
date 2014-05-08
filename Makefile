CSVS=$(wildcard *.csv)

TXTS=$(CSVS:.csv=.ooma.txt)

%.ooma.txt: %.csv
	python google-contacts-to-ooma.py "$<" >"$(basename $<).ooma.txt"

.PHONY: all
all:	$(TXTS)

clean:
	rm -f $(TXTS)

debug:
	echo CSVS=$(CSVS)
	echo TXTS=$(TXTS)
