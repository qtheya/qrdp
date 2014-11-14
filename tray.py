__author__ = 'qtheya'
# -*- coding: utf-8 -*-
from PyQt5 import QtGui, QtCore, QtWidgets
import sys
from index import *
class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, parent)
        if sys.platform == 'win32':
            self.setIcon(QtGui.QIcon("C:\\Users\\qtheya\\PycharmProjects\\wi.png")) #тестовая среда на уинде
        else:
            self.setIcon(QtGui.QIcon.fromTheme("applications-system"))

        self.activated.connect(self.LeftClick)
        self.right_menu = RightClickMenu()
        self.setContextMenu(self.right_menu)

    def LeftClick(self, value):
        if value == QtWidgets.QSystemTrayIcon.Trigger:
            self.mw = MainWindow()
            self.mw.show()

class RightClickMenu(QtWidgets.QMenu):
    def __init__(self, parent=None):
        QtWidgets.QMenu.__init__(self, "Exit", parent)

        icon = QtGui.QIcon.fromTheme("application-exit")
        icon2 = QtGui.QIcon.fromTheme("network-transmit")
        addServ = QtWidgets.QAction(icon2, "&AddServer", self)
        exitAction = QtWidgets.QAction(icon, "&Exit", self)
        exitAction.triggered.connect(lambda : QtWidgets.QApplication.exit(0))
        addServ.triggered.connect(dialogWindow)
        self.addAction(addServ)
        self.addAction(exitAction)
