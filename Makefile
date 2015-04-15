#
# Makefile to build standalone `csql2mongo` Unix-like executable program.
#

FREEZE = cxfreeze
SOURCE = csql2mongo.py
TARGET = csql2mongo

make:
	$(FREEZE) $(SOURCE) --target-dir dist
	
dependencies:
	pip -q install cx_Freeze
	
test:
	sudo mv dist/${TARGET} /usr/bin 
	$(TARGET) -l -f sample.sql
	cat sample.json

clean:
	rm -r -f dist
	rm -r -f $(TARGET)
