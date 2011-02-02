# This represents a bus by number and time

# the time should be a datetime object
import sys
from PySide import QtCore
from PySide import QtGui
from PySide import QtDeclarative

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

class Bus(object):
    def __init__(self, number, arrivetime, destination):
        self.number = number
        self.arrivetime = arrivetime
        self.destination = destination

    def __str__(self):
        return "Number %s Destination %s Time %s" % (self.number, self.destination, self.arrivetime)

buses = [
        Bus("5",  "14:30", "Somewhere with spaces"),
        Bus("26", "16:21", "Left at the lights"),
        Bus("56", "17:01", "Rightfully"),
        Bus("26", "09:21", "Fly"),
        Bus("7",  "13:01", "Hedge SR"),
        ]

app = QtGui.QApplication(sys.argv)
 
m = QtGui.QMainWindow()
 
view = QtDeclarative.QDeclarativeView()
#glw = QtOpenGL.QGLWidget()
#view.setViewport(glw)
view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)

#buses = [BusWrapper(bus) for bus in busdata]
busesListModel = BusListModel(buses)

rc = view.rootContext()

rc.setContextProperty('pythonListModel', busesListModel)

view.setSource('buslist.qml')

m.setCentralWidget(view)
m.show()
app.exec_()
