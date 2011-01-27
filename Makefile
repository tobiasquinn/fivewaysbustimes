# Makefile to build the user interface
UIDIR=fivewaysbustimes/ui

all: $(UIDIR)/MainWindowUI.py

$(UIDIR)/MainWindowUI.py: $(UIDIR)/MainWindowUI.ui
	pyuic4 $(UIDIR)/MainWindowUI.ui -o $(UIDIR)/MainWindowUI.py

clean:
	rm $(UIDIR)/MainWindowUI.py
