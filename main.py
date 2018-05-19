#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#python 3.6.4

from enum import Enum
import sys
import guiPyQt5
import PyQt5.QtWidgets

app = PyQt5.QtWidgets.QApplication(sys.argv)
window = guiPyQt5.MainWindow()

sys.exit(app.exec_())
