#!/usr/bin/python
#simple.py
import sys
from PyQt4 import QtGui
app=QtGui.QApplication(sys.argv)
widget=QtGui.QWidget()
widget.resize(250,250)
widget.setWindowTitle('simple')
widget.show()
sys.exit(app.exec_())
