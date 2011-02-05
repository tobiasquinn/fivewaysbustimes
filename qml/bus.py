# This represents a bus by number and time

# the time should be a datetime object
import sys
from PySide import QtCore
from PySide import QtGui
from PySide import QtDeclarative

from getdata import BusData

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
#        return self._bus.arrivetime.strftime("%H:%M")

    def _destination(self):
        return self._bus.destination

    @QtCore.Signal
    def changed(self): pass

    number = QtCore.Property(unicode, _number, notify=changed)
    arrivetime = QtCore.Property(unicode, _arrivetime, notify=changed)
    destination = QtCore.Property(unicode, _destination, notify=changed)

class BusListModel(QtCore.QAbstractListModel):
    COLUMNS = ('Bus',)

    def __init__(self):
        QtCore.QAbstractListModel.__init__(self)
        self.setRoleNames(dict(enumerate(BusListModel.COLUMNS)))
        self._buses = []

    def setBuses(self, buses):
        self._buses = [BusWrapper(x) for x in buses]
        QtCore.QObject.emit(self, QtCore.SIGNAL("dataChanged(const QtGui.QModelIndex&, const QtGui.QModelIndex &)"), 0, len(self._buses))
        #QtCore.QObject.emit(self, QtCore.SIGNAL("dataChanged(const QtGui.QModelIndex&, const QtGui.QModelIndex &)"), 0, len(self._buses), "banana")
        print "setBuses"
        #self.dataChanged.emit(0, 1)
        #self.dataChanged.emit(QtCore.QModelIndex(0), QtCore.QModelIndex(len(self._buses)))

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
    def __init__(self, number, destination, arrivetime):
        self.number = number
        self.arrivetime = arrivetime
        self.destination = destination

    def __str__(self):
        return "Number %s Destination %s Time %s" % (self.number, self.destination, self.arrivetime)

buses = [
        Bus("5", "Somewhere with spaces", "14:30"),
        Bus("26",  "Left at the lights", "16:21"),
        Bus("56",  "Rightfully", "17:01"),
        Bus("836", "Longbridge", "17:01"),
        Bus("N7",  "Nightfully", "00:21"),
        Bus("N46", "Late", "03:14"),
        Bus("26",  "Fly", "09:21"),
        Bus("7",   "Hedge SR", "13:01"),
        ]
buses1 = [
        Bus("5", "Somewhere with spaces", "13:30"),
        Bus("26",  "Left at the lights", "15:21"),
        Bus("56",  "Rightfully", "16:01"),
        Bus("836", "Longbridge", "19:01"),
        Bus("N7",  "Nightfully", "12:21"),
        Bus("N46", "Late", "05:14"),
        Bus("26",  "Fly", "11:21"),
        Bus("7",   "Hedge SR", "12:01"),
        ]

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.ui = Ui_TestDisplay()
        self.ui.setupUi(self)

        self.display = self.ui.declarativeViewDisplay
        self.display.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
        self._busesListModel = BusListModel()
        rc = self.display.rootContext()
        rc.setContextProperty('pythonListModel', self._busesListModel)
        self.display.setSource('buslist.qml')

        self.ui.pushButtonTest.clicked.connect(self._test)

        self.ui.checkBoxRunTimer.stateChanged.connect(self._runtimer)

        # setup timer
        self._timer = QtCore.QTimer()
        self._timer.setInterval(500)
        self._timer.timeout.connect(self._update)
        # out information source
        #self._businfo = BusData('service.urls')
        self._busesListModel.setBuses(buses)

    def _runtimer(self, state):
        if state:
            self._timer.start()
        else:
            self._timer.stop()

    def _update(self):
        print "Information update"
        data = self._businfo.getData()
        # This needs to be cleaned up
        # load the data into Bus objects
        buses = []
        for x in data:
            buses.append(Bus(x[0], x[1], x[2]))
        self._busesListModel.setBuses(buses)
        print "Data updated"

    def _test(self):
        print "Manual information update"
        #self._update()
        blm = BusListModel()
        blm.setBuses(buses1)
        self.display.rootContext().setContextProperty('pythonListModel', blm)
        #self._busesListModel.setBuses(buses1)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
