#!/usr/bin/python
# messagebox.py
import sys
from PyQt4 import QtGui, QtCore

class MessageBox(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setGeometry(300,300,250, 150)
        self.setWindowTitle('message box')
    def closeEvent(self, event):
        replay=QtGui.QMessageBox.question


