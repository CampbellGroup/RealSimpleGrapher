"""
Window for holding Graphs
"""

import sys
from PyQt5.QtWidgets import *

import GUIConfig
from GraphWidget import PyQTGraphWidget as Graph
from HistWidget import PyQTGraphHistWidget as Hist
from ScrollingGraphWidget import ScrollingPyQTGraphWidget as ScrollingGraph
from ImageWidget import imageWidget as ImageGraph
from GridGraphWindow import GridGraphWindow


class GraphWindow(QTabWidget):
    def __init__(self, reactor, cxn=None, parent=None):
        super(GraphWindow, self).__init__(parent)
        self.cxn = cxn
        self.reactor = reactor
        self.init_ui()
        self.show()

    def init_ui(self):
        reactor = self.reactor

        self.graphDict = {}
        self.tabDict = {}
        self.hidden_tabs = []
        self.parent_lookup = {}
        self.first_plot = {}

        for gc in GUIConfig.tabs:
            gcli = gc.config_list
            gli = []
            sub_names = []
            for config in gcli:
                name = config.name
                max_ds = config.max_datasets
                if config.is_scrolling:
                    g = ScrollingGraph(config, reactor, self.cxn)
                elif config.is_images:
                    g = ImageGraph(config, reactor)
                    self.graphDict[name] = g
                    gli.append(g)
                    continue
                elif config.is_hist:
                    g = Hist(config, reactor, self.cxn)
                    self.graphDict[name] = g
                    gli.append(g)
                    continue
                else:
                    g = Graph(config, reactor, self.cxn)
                g.set_ylimits(config.ylim)
                self.graphDict[name] = g
                gli.append(g)
                sub_names.append(name)
            widget = GridGraphWindow(gli, gc.row_list, gc.column_list, reactor)
            widget.children = sub_names
            for item in sub_names:
                self.first_plot[item] = name
                self.parent_lookup[item] = gc.tab
            self.tabDict[name] = widget
            self.addTab(widget, gc.tab)
            self.setMovable(True)

    def insert_tab(self, t):
        g = Graph(t, reactor)
        self.graphDict[t] = g
        self.addTab(g, t)

    def close_tab(self, current_index):
        current_widget = self.widget(current_index)
        self.hidden_tabs += current_widget.children
        self.removeTab(current_index)

    def insert_closed_tab(self, name):
        first_plot = self.first_plot[name]
        parent_name = self.parent_lookup[name]
        widget = self.tabDict[first_plot]
        index = self.addTab(widget, parent_name)
        self.setCurrentIndex(index)

    def closeEvent(self, x):
        self.reactor.stop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    import qt5reactor

    qt5reactor.install()
    from twisted.internet import reactor

    main = GraphWindow(reactor)
    main.show()
    # noinspection PyUnresolvedReferences
    reactor.run()
