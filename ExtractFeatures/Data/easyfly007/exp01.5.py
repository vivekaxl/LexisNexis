#!/usr/bin/python
#tooltip.py

import sys
from PyQt4 import QtGui, QtCore

class QuirButton(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('quitbutton')
        quit=QtGui.QPushButton('Close', self)
        quit.setGeometry(10,10,60,35)
        self.connect(quit, QtCore.SIGNAL('clicked()'), QtGui.qApp, QtCore.SLOT('quit()'))
app=QtGui.QApplication(sys.argv)
qb=QuirButton()
qb.show()
sys.exit(app.exec_())
