#!/usr/bin/python
#centerpy

import sys
from PyQt4 import QtGui

class Center(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setWindowTitle('center')
        self.resize(250,250)
        self.center()

    def center(self):
        screen=QtGui.QDesktopWidget().screenGeometry()
        size=self.geometry()
        self.move((screen.width()-size.width())/2,
                (screen.height()-size.height())/2)

app=QtGui.QApplication(sys.argv)
qb=Center()
qb.show()
sys.exit(app.exec_())


