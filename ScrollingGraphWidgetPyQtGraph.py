from GraphWidgetPyQtGraph import Graph_PyQtGraph
from PyQt5 import QtGui, QtCore


class ScrollingGraph_PyQtGraph(Graph_PyQtGraph):
    def __init__(self, name, reactor, parent=None, ylim=(0, 1), cxn=None):
        super().__init__(name, reactor, parent)
        self.set_xlimits([0, 100])
        self.pointsToKeep = 100

    def update_figure(self):
        # if len(self.artists) != 0:
        #     # print(self.name, type(self), self.artists)
        #     print(self.name, type(self), "scrolling update_figure")
        x = [0]
        y = [0]
        for ident, params in self.artists.items():
            if params.shown:
                try:
                    index = params.index
                    x = params.dataset.data[:, 0]
                    y = params.dataset.data[:, index+1]
                    params.artist.setData(x, y)
                except TypeError:
                    pass
                except Exception as e:
                    raise e
        try:
            mousepressed = QtGui.QGuiApplication.mouseButtons()
            if (mousepressed == QtCore.Qt.LeftButton) or (mousepressed == QtCore.Qt.RightButton):
                return 
                # see if we need to redraw
            xmin_cur, xmax_cur = self.current_limits
            x_cur = x[-1]  # current largest x value
            window_width = xmax_cur - xmin_cur
            # scroll if we've reached 75% of the window
            if x_cur > (xmin_cur + 0.75*window_width) and (x_cur < xmax_cur):
                shift = (xmax_cur - xmin_cur)/2.0
                xmin = xmin_cur + shift
                xmax = xmax_cur + shift
                self.set_xlimits([xmin, xmax])
        except Exception as e:
            raise e
