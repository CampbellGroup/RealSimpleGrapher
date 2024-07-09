"""
The Real Simple Grapher
"""

from GraphWindow import GraphWindow
from Dataset import Dataset
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QLabel

a = QApplication( [])
import qt5reactor
qt5reactor.install()
#import server libraries
from twisted.internet.defer import returnValue, DeferredLock, Deferred, inlineCallbacks
from twisted.internet.threads import deferToThread
from twisted.internet import reactor
from labrad.server import LabradServer, setting

"""
### BEGIN NODE INFO
[info]
name =  Real Simple Grapher
version = 1.0
description = 
instancename = Real Simple Grapher
[startup]
cmdline = %PYTHON% %FILE%
timeout = 20
[shutdown]
message = 987654321
timeout = 5
### END NODE INFO
"""


class RealSimpleGrapher(LabradServer):
    
    name = "Real Simple Grapher"
    @inlineCallbacks
    def initServer(self):
        self.listeners = set()
        self.gui = GraphWindow(reactor, cxn=self.client)
        self.gui.setWindowTitle('Real Simple Grapher')
        self.gui.setWindowIcon(QtGui.QIcon('icon.png'))
        self.dv = yield self.client.data_vault
        self.pv = yield self.client.parametervault

    def make_dataset(self, dataset_location):
        cxt = self.client.context()
        ds = Dataset(self.dv, cxt, dataset_location, reactor)
        return ds

    def do_plot(self, dataset_location, graph, send_to_current):
        if (graph != 'current') and (send_to_current == True):
            # add the plot to the Current tab as well as an additional
            # specified tab for later examination
            ds = self.make_dataset(dataset_location)
            self.gui.graphDict['current'].add_dataset(ds)
        ds = self.make_dataset(dataset_location)
        if graph in self.gui.hidden_tabs:
            self.gui.insert_closed_tab(graph)
            self.gui.hidden_tabs.remove(graph)
        self.gui.graphDict[graph].add_dataset(ds)
        # tabindex = self.gui.indexOf(self.gui.tabDict[graph])
        # self.gui.setCurrentIndex(tabindex)

    def do_imshow(self, data, image_size, graph, name):
        self.gui.graphDict[graph].update_image(data, image_size, name)

    @setting(1, 'Plot', dataset_location=['(*s, s)', '(*s, i)'], graph='s', send_to_current='b', returns='')
    def plot(self, c, dataset_location, graph, send_to_current=True):
        self.do_plot(dataset_location, graph, send_to_current)

    @setting(2, 'Plot with axis', dataset_location=['(*s, s)', '(*s, i)'], graph='s', axis='*v', send_to_current='b',
             returns='')
    def plot_with_axis(self, c, dataset_location, graph, axis, send_to_current=True):
        minim = min(axis)
        maxim = max(axis)
        if (graph != 'current') and (send_to_current is True):
            self.gui.graphDict['current'].set_xlimits([minim[minim.units], maxim[maxim.units]])
        self.gui.graphDict[graph].set_xlimits([minim[minim.units], maxim[maxim.units]])
        self.do_plot(dataset_location, graph, send_to_current)

    @setting(3, 'Plot image', image='*i', image_size='*i', graph='s', name='s', returns='')
    def plot_image(self, c, image, image_size, graph, name=''):
        self.do_imshow(image, image_size, graph, name)


if __name__ == '__main__':
    from labrad import util

    util.runServer(RealSimpleGrapher())
