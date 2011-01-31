# Makefile to build the user interface
UIDIR=.

all: $(UIDIR)/TestDisplayUI.py $(UIDIR)/TestDisplayUI.py

$(UIDIR)/TestDisplayUI.py: $(UIDIR)/TestDisplayUI.ui
	pyside-uic $(UIDIR)/TestDisplayUI.ui -o $(UIDIR)/TestDisplayUI.py

clean:
	rm $(UIDIR)/TestDisplayUI.py
