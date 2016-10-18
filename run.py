# -*- coding: utf-8 -*-
__author__ = 'erikshe2003'

import sys
from window import mainWindow
from PyQt5 import QtWidgets

app = QtWidgets.QApplication(sys.argv)
mainWindow = mainWindow()
mainWindow.show()
sys.exit(app.exec_())