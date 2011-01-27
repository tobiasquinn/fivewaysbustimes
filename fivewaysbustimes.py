#!/usr/bin/env python

import sys
from PyQt4 import QtGui, QtCore

from fivewaysbustimes.ui.MainWindowUI import Ui_MainWindow

# data feed
from getdata import BusData

class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.connect(self.ui.pushButtonRefresh, QtCore.SIGNAL('clicked()'), self._refreshData)
        self._bd = BusData("service.urls")

    def _refreshData(self):
        print("Refreshing data")
        data = self._bd.getData()
        self.ui.tableWidgetTimes.setRowCount(len(data))
        for i in range(len(data)):
            twiBusnum = QtGui.QTableWidgetItem(data[i][0])
            twiDest   = QtGui.QTableWidgetItem(data[i][1])
            twiArrive = QtGui.QTableWidgetItem(data[i][2].strftime("%H:%M"))

            self.ui.tableWidgetTimes.setItem(i, 1, twiBusnum)
            self.ui.tableWidgetTimes.setItem(i, 2, twiDest)
            self.ui.tableWidgetTimes.setItem(i, 0, twiArrive)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    w = Main()
    w.show()
    sys.exit(app.exec_())
