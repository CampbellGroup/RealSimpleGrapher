import sys
from PyQt5.QtWidgets import *
import pyqtgraph as pg
from TraceListWidget import TraceList
from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.internet.task import LoopingCall
import itertools
import GUIConfig

from RSGDataset import RSGDataset

import queue


class ArtistParameters:
    def __init__(self, artist, dataset, index, shown):
        self.artist = artist
        self.dataset = dataset
        self.index = index
        self.shown = shown
        # update counter in the Dataset object
        # only redraw if the dataset has a higher update count
        self.last_update = 0


class PyQTGraphWidget(QWidget):
    def __init__(self, config, reactor, cxn=None, parent=None):
        # noinspection PyArgumentList
        super().__init__(parent)
        from labrad.units import WithUnit as U

        self.U = U
        self.cxn = cxn
        self.pv = self.cxn.parametervault
        self.reactor = reactor
        self.artists = {}
        self.should_stop = False
        self.name = config.name
        self.vline_name = config.vline
        self.vline_param = config.vline_param
        self.hline_name = config.hline
        self.hline_param = config.hline_param
        self.show_points = config.show_points
        self.grid_on = config.grid_on
        self.scatter_plot = config.scatter_plot

        self.dataset_queue = queue.Queue(config.max_datasets)
        self.pw = pg.PlotWidget()

        lims = self.pw.viewRange()
        self.current_limits = [lims[0][0], lims[0][1]]
        self.live_update_loop = LoopingCall(self.update_figure)
        self.live_update_loop.start(0)

        colors = list(GUIConfig.colors.keys())
        self.colorChooser = itertools.cycle(colors)
        self.init_ui()

    # noinspection PyArgumentList,PyUnresolvedReferences
    @inlineCallbacks
    def init_ui(self):
        self.tracelist = TraceList(self)
        self.pw = pg.PlotWidget()
        if self.vline_name:
            self.inf = pg.InfiniteLine(
                movable=True,
                angle=90,
                label=self.vline_name + "{value:0.0f}",
                labelOpts={
                    "position": 0.9,
                    "color": (200, 200, 100),
                    "fill": (200, 200, 200, 50),
                    "movable": True,
                },
            )
            init_value = yield self.get_init_vline()
            init_value = float(format(init_value[init_value.units], ".4g"))
            self.inf.setValue(init_value)
            self.inf.setPen(width=5.0)

        if self.hline_name:
            self.inf = pg.InfiniteLine(
                movable=True,
                angle=0,
                label=self.hline_name + "{value:0.0f}",
                labelOpts={
                    "position": 0.9,
                    "color": (200, 200, 100),
                    "fill": (200, 200, 200, 50),
                    "movable": True,
                },
            )
            init_value = yield self.get_init_hline()
            self.inf.setValue(init_value)
            self.inf.setPen(width=5.0)

        self.coords = QLabel("")
        self.title = QLabel(self.name)
        frame = QFrame()
        splitter = QSplitter()
        splitter.addWidget(self.tracelist)
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        vbox.addWidget(self.title)
        vbox.addWidget(self.pw)
        vbox.addWidget(self.coords)
        frame.setLayout(vbox)
        splitter.addWidget(frame)
        hbox.addWidget(splitter)
        self.setLayout(hbox)
        # self.legend = self.pw.addLegend()
        self.tracelist.itemChanged.connect(self.checkbox_changed)
        self.pw.plot([], [])
        vb = self.pw.plotItem.vb
        self.img = pg.ImageItem()
        vb.addItem(self.img)

        if self.vline_name:
            vb.addItem(self.inf)
            self.inf.sigPositionChangeFinished.connect(self.vline_changed)

        if self.hline_name:
            vb.addItem(self.inf)
            self.inf.sigPositionChangeFinished.connect(self.hline_changed)

        self.pw.scene().sigMouseMoved.connect(self.mouse_moved)
        self.pw.sigRangeChanged.connect(self.range_changed)

    def get_item_color(self, color):
        return GUIConfig.colors[color]

    def update_figure(self):
        for ident, params in self.artists.items():
            if params.shown:
                ds = params.dataset
                index = params.index
                current_update = ds.updateCounter
                if params.last_update < current_update and ds.data is not None:
                    x = ds.data[:, 0]
                    y = ds.data[:, index + 1]
                    params.last_update = current_update
                    params.artist.setData(x, y)

    def add_artist(self, ident, dataset, index, no_points=False):
        """
        no_points is an override parameter to the global show_points setting.
        It is to allow data fits to be plotted without points
        """
        new_color = next(self.colorChooser)
        if self.show_points and not no_points:
            line = self.pw.plot(
                [],
                [],
                symbol="o",
                symbolBrush=self.get_item_color(new_color),
                name=ident,
                pen=self.get_item_color(new_color),
                connect=self.scatter_plot,
            )
        else:
            line = self.pw.plot([], [], pen=self.get_item_color(new_color), name=ident)
        if self.grid_on:
            self.pw.showGrid(x=True, y=True)
        self.artists[ident] = ArtistParameters(line, dataset, index, True)
        self.tracelist.addTrace(ident, new_color)

    def remove_artist(self, ident):
        try:
            artist = self.artists[ident].artist
            self.pw.removeItem(artist)
            # self.legend.removeItem(ident)
            self.tracelist.removeTrace(ident)
            self.artists[ident].shown = False
            try:
                del self.artists[ident]
            except KeyError:
                pass
        except Exception as e:
            print("remove artist failed")
            print(e)

    def display(self, ident, shown):
        try:
            artist = self.artists[ident].artist
            if shown:
                self.pw.addItem(artist)
                self.artists[ident].shown = True
            else:
                self.pw.removeItem(artist)
                # self.legend.removeItem(ident)
                self.artists[ident].shown = False
        except KeyError:
            raise Exception("404 Artist not found")

    def checkbox_changed(self):
        for ident, item in self.tracelist.trace_dict.items():
            try:
                if item.checkState() and not self.artists[ident].shown:
                    self.display(ident, True)
                if not item.checkState() and self.artists[ident].shown:
                    self.display(ident, False)
            except KeyError:  # this means the artist has been deleted.
                pass

    def range_changed(self):
        lims = self.pw.viewRange()
        self.pointsToKeep = lims[0][1] - lims[0][0]
        self.current_limits = [lims[0][0], lims[0][1]]

    @inlineCallbacks
    def add_dataset(self, dataset: RSGDataset):
        try:
            self.dataset_queue.put(dataset, block=False)
        except queue.Full:
            remove_ds = self.dataset_queue.get()
            self.remove_dataset(remove_ds)
            self.dataset_queue.put(dataset, block=False)
        labels = yield dataset.get_labels()
        for i, label in enumerate(labels):
            self.add_artist(label, dataset, i)

    @inlineCallbacks
    def remove_dataset(self, dataset):
        labels = yield dataset.get_labels()
        for label in labels:
            self.remove_artist(label)

    def set_xlimits(self, limits):
        self.pw.setXRange(limits[0], limits[1])
        self.current_limits = limits

    def set_ylimits(self, limits):
        self.pw.setYRange(limits[0], limits[1])

    def mouse_moved(self, pos):
        pnt = self.img.mapFromScene(pos)
        string = "(" + str(pnt.x()) + " , " + str(pnt.y()) + ")"
        self.coords.setText(string)

    @inlineCallbacks
    def get_init_vline(self):
        init_vline = yield self.pv.get_parameter(
            self.vline_param[0], self.vline_param[1]
        )
        returnValue(init_vline)

    @inlineCallbacks
    def get_init_hline(self):
        init_hline = yield self.pv.get_parameter(
            self.hline_param[0], self.hline_param[1]
        )
        returnValue(init_hline)

    @inlineCallbacks
    def vline_changed(self, sig):
        val = self.inf.value()
        param = yield self.pv.get_parameter(self.vline_param[0], self.vline_param[1])
        units = param.units
        val = self.U(val, units)
        yield self.pv.set_parameter(self.vline_param[0], self.vline_param[1], val)

    @inlineCallbacks
    def hline_changed(self, sig):
        val = self.inf.value()
        param = yield self.pv.get_parameter(self.hline_param[0], self.hline_param[1])
        units = param.units
        val = self.U(val, units)
        yield self.pv.set_parameter(self.hline_param[0], self.hline_param[1], val)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    import qt5reactor

    qt5reactor.install()
    from twisted.internet import reactor

    # noinspection PyTypeChecker
    main = PyQTGraphWidget("example", reactor)
    main.show()
    # noinspection PyUnresolvedReferences
    reactor.run()
