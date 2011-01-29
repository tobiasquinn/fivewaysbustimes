# Makefile to build the user interface
UIDIR=fivewaysbustimes/ui

all: $(UIDIR)/MainWindowUI.py $(UIDIR)/GraphicsUI.py

$(UIDIR)/MainWindowUI.py: $(UIDIR)/MainWindowUI.ui
	pyuic4 $(UIDIR)/MainWindowUI.ui -o $(UIDIR)/MainWindowUI.py

$(UIDIR)/GraphicsUI.py: $(UIDIR)/GraphicsUI.ui
	pyuic4 $(UIDIR)/GraphicsUI.ui -o $(UIDIR)/GraphicsUI.py

clean:
	rm $(UIDIR)/MainWindowUI.py
	rm $(UIDIR)/GraphicsUI.py
