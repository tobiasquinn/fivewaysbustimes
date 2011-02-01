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

    def _name(self):
        return str(self._bus)

    changed = QtCore.Signal()
    name = QtCore.Property(unicode, _name, notify=changed)

class BusListModel(QtCore.QAbstractListModel):
    COLUMNS = ('Number', 'Time')

    def __init__(self, busdata):
        QtCore.QAbstractListModel.__init__(self)
        self._busdata = busdata
        self.setRoleNames(dict(enumerate(BusListModel.COLUMNS)))

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._busdata)

    def data(self, index, role):
        if index.isValid() and role == ThingListModel.COLUMNS.index('Number'):
            return self._busdata[index.row]
        return None

class Bus(object):
    def __init__(self, number, arrivetime):
        self.number = number
        self.arrivetime = arrivetime

    def __str__(self):
        return "Number %d Time %s" % (self.number, self.arrivetime)

busdata = [
        Bus(5,  "14:30"),
        Bus(26, "16:21"),
        Bus(56, "17:01"),
        Bus(26, "09:21"),
        Bus(7,  "13:01"),
        ]

app = QtGui.QApplication(sys.argv)
 
m = QtGui.QMainWindow()
 
view = QtDeclarative.QDeclarativeView()
#glw = QtOpenGL.QGLWidget()
#view.setViewport(glw)
view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)

buses = [BusWrapper(bus) for bus in busdata]
busesList = BusListModel(buses)

rc = view.rootContext()

rc.setContextProperty('pythonListModel', busesList)

view.setSource('buslist.qml')

m.setCentralWidget(view)
m.show()
app.exec_()
