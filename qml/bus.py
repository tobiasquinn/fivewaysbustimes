# This represents a bus by number and time

# the time should be a datetime object
import sys
from PySide import QtCore
from PySide import QtGui
from PySide import QtDeclarative

from getdata import BusData

# use the same as testdisplay.py
from TestDisplayUI import Ui_TestDisplay

class Bus(QtCore.QObject):
    def __init__(self, number, destination, arrivetime):
        QtCore.QObject.__init__(self)
        self._number = number
        self._destination = destination
        self._arrivetime = arrivetime

    def getNumber(self):
        return self._number

    def getArrivetime(self):
#        return self._arrivetime
        return self._arrivetime.strftime("%H:%M")

    def getDestination(self):
        return self._destination

    def set(self, new):
        print "Bus::set"
        print self, new
        self._number = new._number
        self._arrivetime = new._arrivetime
        self._destination = new._destination
        self.changed.emit()

    @QtCore.Signal
    def changed(self):
        pass
        print "BusWrapper::changed"

    def __cmp__(self, other):
        print "%s~%s %s~%s %s~%s" % (self.getNumber(), other.getNumber(), self.getArrivetime(), other.getArrivetime(), self.getDestination(), other.getDestination())
        if other.getNumber() == self.getNumber() and other.getArrivetime() == self.getArrivetime() and other.getDestination() == self.getDestination():
            return 0
        else:
            return -1

    number = QtCore.Property(unicode, getNumber, notify=changed)
    arrivetime = QtCore.Property(unicode, getArrivetime, notify=changed)
    destination = QtCore.Property(unicode, getDestination, notify=changed)

class BusListModel(QtCore.QAbstractListModel):
    COLUMNS = ('Bus',)

    def __init__(self, buses=[]):
        QtCore.QAbstractListModel.__init__(self)
        self.setRoleNames(dict(enumerate(BusListModel.COLUMNS)))
        self._buses = buses

    def setBuses(self, buses):
        print "setBuses"
        # catch initialisation (this should really be in __init__)
        #try:
        #    self._buses
        #except AttributeError:
        #    self._buses = [BusWrapper(x) for x in buses]
        #    return
        # take a list of Bus objects
        # compare each one to held list of bus objects
        # remove any extra
        newlen = len(buses)
        oldlen = len(self._buses)
        if newlen < oldlen:
            # remove extra rows
            print newlen, oldlen - newlen
            self._removeRows(newlen, oldlen - newlen)
            for i in range(oldlen, newlen, -1):
                print "del %d" % i
        # FIXME: we should catch the first row(s) being removed?
        elif newlen > oldlen:
            print newlen, newlen - oldlen
            for i in range(oldlen, newlen):
                print "add %d" % i
                self._appendRow(buses[i], i)
        # we've now dealy with additions
        # set any rows that have changed
        for i in range(newlen):
            bus = buses[i]
            if self._buses[i] != bus:
                print "change %d" % i
                self._set(i, bus)
            
        # if a row is different or new then use the set method
        # this must run from 0 upwards

    def _set(self, row, bus):
        # set or create a bus object on the appropriate row
        print "set"
        # should do checks for index sanity
        self._buses[row].set(bus)

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._buses)

    def data(self, index, role):
        if index.isValid() and role == BusListModel.COLUMNS.index('Bus'):
            return self._buses[index.row()]
        return None

    def _appendRow(self, bus, row, parent=QtCore.QModelIndex()):
        print "_appendRow"
        self.beginInsertRows(parent, row, row)
        self._buses.append(bus)
        self.endInsertRows()

    def _removeRows(self, row, count, parent=QtCore.QModelIndex()):
        print "_removeRows"
        self.beginRemoveRows(parent, row, row + count - 1)
        while count != 0:
            del self._buses[row]
            count -= 1
        self.endRemoveRows()
        return True

from copy import copy
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

        self.ui.pushButtonTestBuses1.clicked.connect(self._testbuses1)
        self.ui.pushButtonTestBuses2.clicked.connect(self._testbuses2)
        self.ui.pushButtonManualFetch.clicked.connect(self._manualfetch)

        self.ui.checkBoxRunTimer.stateChanged.connect(self._runtimer)

        # setup timer
        self._timer = QtCore.QTimer()
        self._timer.setInterval(30 * 1000)
        self._timer.timeout.connect(self._update)
        # out information source
        self._businfo = BusData('service.urls')

    def _runtimer(self, state):
        if state:
            self._timer.start()
        else:
            self._timer.stop()

    def _manualfetch(self):
        print "Manual fetch"
        self._update()

    def _update(self):
        print "Information update"
        data = self._businfo.getData()
        # This needs to be cleaned up
        # load the data into Bus objects
        buses = []
        for x in data:
            buses.append(Bus(x[0], x[1], x[2]))
        print buses
        self._busesListModel.setBuses(buses)
        print "Data updated"

    def _testbuses1(self):
        #print "Manual information update"
        print "Buses 1"
        self._busesListModel.setBuses((
                Bus("5", "Somewhere with spaces", "14:30"),
                Bus("26",  "Left at the lights", "16:21"),
                Bus("56",  "Rightfully", "17:01"),
                Bus("836", "Longbridge", "17:01"),
                Bus("N7",  "Nightfully", "00:21"),
                Bus("N46", "Late", "03:14"),
                Bus("26",  "Fly", "09:21"),
                Bus("7",   "Hedge SR", "13:01"),
                ))

    def _testbuses2(self):
        print "Buses 2"
        self._busesListModel.setBuses((
                Bus("5", "Somewhere with spaces", "13:30"),
                Bus("26",  "Left at the lights", "16:21"),
                Bus("56",  "Rightfully", "16:01"),
                Bus("836", "Longbridge", "19:01"),
                Bus("N7",  "Nightfully", "00:21"),
                Bus("N46", "Late", "05:14"),
                Bus("26",  "Fly", "11:21"),
                Bus("7",   "Hedge SR", "12:01"),
                ))

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
