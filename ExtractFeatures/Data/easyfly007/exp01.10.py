#~/use/bin/python
#menubar.py

import sys
from PyQt4 import QtGui, QtCore

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self)
        self,resize(250,150)
        self.setWindowTitle('menubar')

        exit=QtGui.QAction(QtGui.QIcon('icons/exit.png'), 'Exit', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit application')
        exit.connect(exit, QtCore.SIGNAL('triggered()'), QtGui.qApp,
                QtCore.SLOT('quit()'))
        self,statusBar()
        menubar=self,menuBar()
        file=menubar.addMenu('&File')
        file.addAction(exit)

app=QtGui.QApplicaiton(sys.argv)
main=MainWindow()
main.show()
sys.exit(app.exec_())

