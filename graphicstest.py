#!/usr/bin/python2
import sys
from PyQt4 import QtGui, QtCore

from fivewaysbustimes.ui.GraphicsUI import Ui_Graphics

class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.ui = Ui_Graphics()
        self.ui.setupUi(self)

        #self.connect(self.ui.pushButtonStart, QtCore.SIGNAL('clicked()'), self._start)
        self._setupstatemachine()

        self.connect(self.ui.pushButtonA, QtCore.SIGNAL('clicked()'), self._A)
        self.connect(self.ui.pushButtonB, QtCore.SIGNAL('clicked()'), self._B)

    def _A(self):
        print "A"
        self._goe.setOpacity(0.0)

    def _B(self):
        print "B"
        self._goe.setOpacity(1.0)

    def _setupstatemachine(self):
        # define out opacity states
        self._goe = QtGui.QGraphicsOpacityEffect()
        self.ui.labelTest.setGraphicsEffect(self._goe)

        # setup our states
        startState = QtCore.QState()
        startState.assignProperty(self._goe, 'opacity', 0.0)

        endState = QtCore.QState()
        endState.assignProperty(self._goe, 'opacity', 1.0)

        # set a transistion
#        trans = QtCore.QSignalTransition(self.ui.pushButtonStart, QtCore.SIGNAL('clicked()'))
#        trans.setTargetState(endState)
        startState.addTransition(self.ui.pushButtonStart, QtCore.SIGNAL('clicked()'), endState)
        endState.addTransition(self.ui.pushButtonStart, QtCore.SIGNAL('clicked()'), startState)

        # add these states to the machine
        machine = QtCore.QStateMachine()
        machine.addState(startState)
        machine.addState(endState)
        machine.setInitialState(startState)

        pa = QtCore.QPropertyAnimation(self._goe, 'opacity')
        pa.setEasingCurve(QtCore.QEasingCurve.Linear)
        pa.setDuration(1000)
        machine.addDefaultAnimation(pa)
        machine.start()
        print "Set state machine"

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    w = Main()
    w.show()
    sys.exit(app.exec_())
