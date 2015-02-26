#!/usr/bin/python
#tooltip.py

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore

class Tooltip(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setGeometry(900,100,450,150)
        self.setWindowTitle("Too2ltip")
        self.setToolTip('This is a <b> QWidget</b> widget')
        QtGui.QToolTip.setFont(QtGui.QFont('OldEnglish',10))
app=QtGui.QApplication(sys.argv)
tooltip=Tooltip()
tooltip.show()
sys.exit(app.exec_())
