from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget

from twisted.internet.defer import inlineCallbacks
import socket


class DataVaultList(QWidget):

    def __init__(self, tracename, parent=None):
        super(DataVaultList, self).__init__()
        self.tracename = tracename
        self.connect()

    @inlineCallbacks
    def connect(self):
        from labrad.wrappers import connectAsync

        self.cxn = yield connectAsync(name=socket.gethostname() + " Data Vault Client")
        self.grapher = yield self.cxn.real_simple_grapher
        self.dv = yield self.cxn.data_vault
        self.initializeGUI()

    def initializeGUI(self):
        mainLayout = QVBoxLayout()
        self.dataListWidget = QListWidget()
        self.dataListWidget.doubleClicked.connect(self.onDoubleclick)
        mainLayout.addWidget(self.dataListWidget)
        self.setWindowTitle("Data Vault")
        self.setLayout(mainLayout)
        self.populate()
        self.show()

    @inlineCallbacks
    def populate(self):
        self.dataListWidget.clear()
        ls = yield self.dv.dir()
        self.dataListWidget.addItem("...")
        self.dataListWidget.addItems(sorted(ls[0]))
        if ls[1] is not None:
            self.dataListWidget.addItems(sorted(ls[1]))

    @inlineCallbacks
    def onDoubleclick(self, item):
        item = self.dataListWidget.currentItem().text()
        if item == "...":
            yield self.dv.cd(1)
            self.populate()
        else:
            try:
                yield self.dv.cd(str(item))
                self.populate()
            except:
                path = yield self.dv.cd()
                yield self.grapher.plot((path, str(item)), self.tracename, False)

    def closeEvent(self, event):
        self.cxn.disconnect()
