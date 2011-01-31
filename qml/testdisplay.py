#!/usr/bin/python2

import sys
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtDeclarative import QDeclarativeView

from TestDisplayUI import Ui_TestDisplay

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        
        self.ui = Ui_TestDisplay()
        self.ui.setupUi(self)

        self.display = self.ui.declarativeViewDisplay
        self.display.setSource(QUrl.fromLocalFile('display.qml'))
        self.display.show()
        # QML resizes to main window
        #self.setResizeModel(QDeclarativeView.SizeRootObjectToView)
        self.ui.pushButtonTest.clicked.connect(self._test)

    def _test(self):
        print "Test"
        print self.display
        self._text = self.display.rootContext()
        print self._text
        print dir(self._text)
        print self._text.contextProperty('color')
        self._text.setContextProperty("text", "123456")
        self._text.setContextProperty("color", "black")

if __name__ == '__main__':
    # Create application and the view
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # Enter mainloop
    sys.exit(app.exec_())

