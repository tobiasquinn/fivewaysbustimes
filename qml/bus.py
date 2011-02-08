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

    def set(self, new):
        self._number = new._number
        self._arrivetime = new._arrivetime
        self._destination = new._destination
        self.changed.emit()

    @QtCore.Signal
    def changed(self):
        print "BusWrapper::changed"
        pass

    def __cmp__(self, other):
        print self._number(), other._number()
        print self._arrivetime(), other._arrivetime()
        print self._destination(), other._destination()
        if other._number() == self._number() and other._arrivetime() == self._arrivetime() and other._destination() == self._destination():
            return 0
        else:
            return -1

    def testchanged(self):
        print self
        self.changed.emit()

    number = QtCore.Property(unicode, _number, notify=changed)
    arrivetime = QtCore.Property(unicode, _arrivetime, notify=changed)
    destination = QtCore.Property(unicode, _destination, notify=changed)

class BusListModel(QtCore.QAbstractListModel):
    COLUMNS = ('Bus',)

    def __init__(self, buses=[]):
        QtCore.QAbstractListModel.__init__(self)
        self.setRoleNames(dict(enumerate(BusListModel.COLUMNS)))
        self._buses = [BusWrapper(x) for x in buses]

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
                self._appendRow(BusWrapper(buses[i]), i)
        # we've now dealy with additions
        # set any rows that have changed
        for i in range(newlen):
            bus = BusWrapper(buses[i])
            print self._buses[i], bus
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
        Bus("26",  "Left at the lights", "16:21"),
        Bus("56",  "Rightfully", "16:01"),
        Bus("836", "Longbridge", "19:01"),
        Bus("N7",  "Nightfully", "00:21"),
        Bus("N46", "Late", "05:14"),
        Bus("26",  "Fly", "11:21"),
        Bus("7",   "Hedge SR", "12:01"),
        ]
#buses1 = [
#        Bus("5", "Somewhere with spaces", "13:30"),
#        Bus("26",  "Left at the lights", "16:21"),
#        Bus("56",  "Rightfully", "16:01"),
#        ]

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

        self.ui.pushButtonTestAdd.clicked.connect(self._testadd)
        self.ui.pushButtonTestRemove.clicked.connect(self._testremove)
        self.ui.pushButtonChange.clicked.connect(self._testchange)

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

    def _testremove(self):
        #print "Manual information update"
        print "Test remove"
        self._busesListModel.setBuses(buses1)

    def _testadd(self):
        print "Test add"
        self._busesListModel.setBuses(buses)

    def _testchange(self):
        print "Test Change"
        l = buses1
        l[1] = Bus("99", "LAOIRK", "55:55")
        print l
        self._busesListModel.setBuses(l)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
