#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import system
import sys
from PyQt5 import QtGui, QtCore, QtWidgets

settings = QtCore.QSettings()
settings.setValue('servers', {})
settings.setValue('credentials', {})

del settings
settings = QtCore.QSettings()
servers = settings.value('servers', type = QtCore.QVariant)
credentials = settings.value('credentials', type = QtCore.QVariant)



def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("qrdp")
    global mw
    mw = MainWindow()
    mw.show()
    trayWidget = SystemTrayIcon()
    trayWidget.show()
    sys.exit(app.exec_())


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle('qrdp')
        self.addButton = QtWidgets.QPushButton('New connection')
        self.addButton.clicked.connect(self.addWidget)
        self.cb = QtWidgets.QCheckBox('Remove host', self)
        self.resolution = QtWidgets.QLineEdit(self)
        self.resolution.setObjectName("resolution")
        self.resolution.setText("1366x695")
        self.scrollLayout = QtWidgets.QFormLayout()
        self.scrollWidget = QtWidgets.QWidget()
        self.scrollWidget.setLayout(self.scrollLayout)
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollWidget)
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addWidget(self.addButton)
        self.mainLayout.addWidget(self.resolution)
        self.mainLayout.addWidget(self.cb)
        self.check = False

        for item in servers:
            srv = servers.get(item)
            btn = QtWidgets.QPushButton(srv, self)
            btn.clicked.connect(self.buttonClicked)
            btn.resize(btn.sizeHint())
            btn.setToolTip(srv)
            self.scrollLayout.addRow(btn)

        self.mainLayout.addWidget(self.scrollArea)
        self.centralWidget = QtWidgets.QWidget()
        self.centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.centralWidget)
        self.cb.stateChanged.connect(self.cb_changed)

    def addWidget(self):
        if mw.isHidden() == True:
            mw.show()
        self.scrollLayout.addRow(newHostButton())

    def cb_changed(self, state):
        self.check = (state == QtCore.Qt.Checked)

    def closeEvent(self, event):
       event.ignore()
       self.hide()

    def buttonClicked(self):
        sender = self.sender()
        host = sender.text()
        print host
        if self.check is True:
            sender.deleteLater()
            for k,v in servers.items():
                if v == host:
                    del servers[k]
        else:
            authSettings = credentials.get(host)
            user = authSettings[0]
            user = str(user)
            password =  authSettings[1]
            password = str(password)
            isadm = authSettings[2]
            system("rdesktop -5 -K -r clipboard:CLIPBOARD -z -a 16 " + host +'' + isadm + " -g " + self.resolution.text() + " -u " + user + " -p " +password)


class dialogWindow(QtWidgets.QDialog):
    def __init__(self):
        super(dialogWindow, self).__init__()
        self.setFixedSize(220,330)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.textName = QtWidgets.QLineEdit(self)
        self.textPass = QtWidgets.QLineEdit(self)
        self.textHost = QtWidgets.QLineEdit(self)
        self.textName.setObjectName("Username")
        self.textName.setText("Username")
        self.textPass.setObjectName("Password")
        self.textPass.setText("Password")
        self.textHost.setObjectName("Hostname")
        self.textHost.setText("Hostname")
        self.textPass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.cb = QtWidgets.QCheckBox('/admin', self)
        self.cb.move(140, 120)
        self.cb.stateChanged.connect(self.adminSession)
        self.cb.resize(self.cb.sizeHint())
        self.cb1 = QtWidgets.QCheckBox("Administrator", self)
        self.cb1.move(10, 120)
        self.cb1.resize(self.cb1.sizeHint())
        self.cb1.stateChanged.connect(self.admin)
        self.isadm = ''
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.textHost)
        layout.addWidget(self.textName)
        layout.addWidget(self.textPass)

        self.addButton = QtWidgets.QPushButton('Add server', self)
        self.addButton.resize(self.addButton.sizeHint())
        self.addButton.move(10, 10)
        self.addButton.clicked.connect(self.addHost)
        self.closeButton = QtWidgets.QPushButton('Cancel', self)
        self.closeButton.clicked.connect(self.deleteLater)
        self.closeButton.resize(self.closeButton.sizeHint())
        self.closeButton.move(120, 10)
        self.setGeometry(300, 300, 225, 350)
        self.exec_()

    def adminSession(self, state):
        if state == QtCore.Qt.Checked:
            isadm = ' -0'
            self.isadm = isadm

    def admin(self, st):
        if st == QtCore.Qt.Checked:
            self.textName.setText("Administrator")
            self.cb.toggle()


    def addHost(self):
        host = self.textHost.text()
        name = self.textName.text()
        password = self.textPass.text()
        servlen = range(1, 1000)
        newItem = [x for x in servlen if x not in servers.keys()]
        servers.update({newItem[0] : host})
        newHost = servers.get(newItem[0])
        credentials.update({newHost : [name, password, self.isadm]})
        self.accept()


class newHostButton(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super(newHostButton, self).__init__(parent)
        a = dialogWindow()
        self.setText(a.textHost.text())
        self.clicked.connect(mw.buttonClicked)


class delWindow(QtWidgets.QDialog):
    def __init__(self):
        super(delWindow, self).__init__()
        x = 10
        y = 50
        for item in servers:
            srv = servers.get(item)
            btn = QtWidgets.QPushButton(srv, self)
            btn.clicked.connect(self.deleteLater)
            btn.resize(btn.sizeHint())
            btn.move(x, y)
            self.setToolTip(srv)
            y += 40
        self.setGeometry(300, 300, 225, 350)
        self.exec_()


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, parent)
        self.setIcon(QtGui.QIcon.fromTheme("applications-system"))

        self.activated.connect(self.LeftClick)
        self.right_menu = RightClickMenu()
        self.setContextMenu(self.right_menu)

    def LeftClick(self, value):
        if value == QtWidgets.QSystemTrayIcon.Trigger:
            mw.show()

class RightClickMenu(QtWidgets.QMenu):
    def __init__(self, parent=None):
        super(RightClickMenu, self).__init__(parent)
        icon = QtGui.QIcon.fromTheme("application-exit")
        icon2 = QtGui.QIcon.fromTheme("network-transmit")
        addServ = QtWidgets.QAction(icon2, "&AddServer", self)
        exitAction = QtWidgets.QAction(icon, "&Exit", self)
        exitAction.triggered.connect(QtWidgets.QApplication.exit)
        addServ.triggered.connect(mw.addWidget)
        self.addAction(addServ)
        self.addAction(exitAction)


if __name__ == '__main__':
    main()



