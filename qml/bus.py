# This represents a bus by number and time

# the time should be a datetime object
import sys
from PySide import QtCore
from PySide import QtGui
from PySide import QtDeclarative

# use the same as testdisplay.py
from TestDisplayUI import Ui_TestDisplay

class BusWrapper(QtCore.QObject):
    def __init__(self, bus):
        QtCore.QObject.__init__(self)
        self._bus = bus

    def _number(self):
        return self._bus.number

    def _arrivetime(self):
        return self._bus.arrivetime

    def _destination(self):
        return self._bus.destination

    @QtCore.Signal
    def changed(self): pass

    number = QtCore.Property(unicode, _number, notify=changed)
    arrivetime = QtCore.Property(unicode, _arrivetime, notify=changed)
    destination = QtCore.Property(unicode, _destination, notify=changed)

class BusListModel(QtCore.QAbstractListModel):
    COLUMNS = ('Bus',)

    def __init__(self, buses):
        QtCore.QAbstractListModel.__init__(self)
        self._buses = [BusWrapper(x) for x in buses]
        self.setRoleNames(dict(enumerate(BusListModel.COLUMNS)))

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._buses)

    def data(self, index, role):
        if index.isValid() and role == BusListModel.COLUMNS.index('Bus'):
            return self._buses[index.row()]
        return None

    def removeRows(self, row, count, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, row, row + count - 1)
        while count != 0:
            del self._buses[row]
            count -= 1
        self.endRemoveRows()
        return True

class Bus(object):
    def __init__(self, number, arrivetime, destination):
        self.number = number
        self.arrivetime = arrivetime
        self.destination = destination

    def __str__(self):
        return "Number %s Destination %s Time %s" % (self.number, self.destination, self.arrivetime)

buses = [
        Bus("5",   "14:30", "Somewhere with spaces"),
        Bus("26",  "16:21", "Left at the lights"),
        Bus("56",  "17:01", "Rightfully"),
        Bus("836", "17:01", "Longbridge"),
        Bus("N7",  "00:21", "Nightfully"),
        Bus("N46", "03:14", "Late"),
        Bus("26",  "09:21", "Fly"),
        Bus("7",   "13:01", "Hedge SR"),
        ]

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.ui = Ui_TestDisplay()
        self.ui.setupUi(self)

        self.display = self.ui.declarativeViewDisplay
        self.display.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
        self.busesListModel = BusListModel(buses)
        rc = self.display.rootContext()
        rc.setContextProperty('pythonListModel', self.busesListModel)
        self.display.setSource('buslist.qml')

        self.ui.pushButtonTest.clicked.connect(self._test)

    def _test(self):
        print "Test clicked"
        print self.busesListModel.removeRow(2)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
