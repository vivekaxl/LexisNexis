#!/usr/bin/python
#statusbar.py

import sys
from PyQt4 import QtGui

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.resize(250, 150)
        self.setWindowTitle('statusbar')
        self.statusBar().showMessage('Ready')

app=QtGui.QApplication(sys.argv)
main=MainWindow()
main.show()
sys.exit(app.exec_())

