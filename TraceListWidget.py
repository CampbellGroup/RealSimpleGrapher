from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import *

from ParameterListWidget import ParameterList
from DataVaultListWidget import DataVaultList
from FitWindowWidget import FitWindow
from PredictSpectrumWidget import PredictSpectrum
from GUIConfig import traceListConfig, colors


class TraceList(QListWidget):
    def __init__(self, parent):
        super(TraceList, self).__init__()
        self.parent = parent
        self.windows = []
        self.config = traceListConfig()
        self.setStyleSheet("background-color:%s;" % self.config.background_color)
        try:
            self.use_trace_color = self.config.use_trace_color
        except AttributeError:
            self.use_trace_color = False

        self.name = 'pmt'
        self.initUI()

    def initUI(self):
        self.trace_dict = {}
        item = QListWidgetItem('Traces')
        item.setCheckState(QtCore.Qt.Checked)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.popupMenu)


    def addTrace(self, ident, color):
        item = QListWidgetItem(ident)

        if self.use_trace_color:
            foreground_color = self.parent.get_item_color(color)
            item.setForeground(foreground_color)
        else:
            item.setForeground(QtGui.QColor(255, 255, 255))
        item.setBackground(QtGui.QColor(0, 0, 0))

        item.setCheckState(QtCore.Qt.Checked)
        self.addItem(item)
        self.trace_dict[ident] = item

    def removeTrace(self, ident):
        item = self.trace_dict[ident]
        row = self.row(item)
        self.takeItem(row)
        item = None

    def changeTraceListColor(self, ident, new_color):
        item = self.trace_dict[ident]
        item.setForeground(new_color)

    def popupMenu(self, pos):
        menu = QMenu()
        item = self.itemAt(pos)
        if item is None:
            dataaddAction = menu.addAction('Add Data Set')
            spectrumaddAction = menu.addAction('Add Predicted Spectrum')

            action = menu.exec_(self.mapToGlobal(pos))
            if action == dataaddAction:
                dvlist = DataVaultList(self.parent.name)
                self.windows.append(dvlist)
                dvlist.show()

            if action == spectrumaddAction:
                ps = PredictSpectrum(self)
                self.windows.append(ps)
                ps.show()

        else:
            ident = str(item.text())
            parametersAction = menu.addAction('Parameters')
            togglecolorsAction = menu.addAction('Toggle colors')
            fitAction = menu.addAction('Fit')
            selectColorMenu = menu.addMenu("Select color")
            redAction = selectColorMenu.addAction("red")
            greenAction = selectColorMenu.addAction("green")
            yellowAction = selectColorMenu.addAction("yellow")
            blueAction = selectColorMenu.addAction("blue")
            orangeAction = selectColorMenu.addAction("orange")
            purpleAction = selectColorMenu.addAction("purple")
            cyanAction = selectColorMenu.addAction("cyan")
            magentaAction = selectColorMenu.addAction("magenta")
            limeAction = selectColorMenu.addAction("lime")
            pinkAction = selectColorMenu.addAction("pink")
            tealAction = selectColorMenu.addAction("teal")
            lavenderAction = selectColorMenu.addAction("lavender")
            colorActionDict = {redAction: colors["red"],
                               greenAction: colors["green"],
                               yellowAction: colors["yellow"],
                               blueAction: colors["blue"],
                               orangeAction: colors["orange"],
                               purpleAction: colors["purple"],
                               cyanAction: colors["cyan"],
                               magentaAction: colors["magenta"],
                               limeAction: colors["lime"],
                               pinkAction: colors["pink"],
                               tealAction: colors["teal"],
                               lavenderAction: colors["lavender"]}

            action = menu.exec_(self.mapToGlobal(pos))
            
            if action == parametersAction:
                # option to show parameters in separate window
                dataset = self.parent.artists[ident].dataset
                pl = ParameterList(dataset)
                self.windows.append(pl)
                pl.show()

            if action == togglecolorsAction:               
                # option to change color of line
                new_color = colors[next(self.parent.colorChooser)]
                self.parent.artists[ident].artist.setPen(new_color, symbolBrush=new_color)
                self.changeTraceListColor(ident, new_color)

            if action == fitAction:
                dataset = self.parent.artists[ident].dataset
                index = self.parent.artists[ident].index
                fw = FitWindow(dataset, index, self)
                self.windows.append(fw)
                fw.show()

            if action in colorActionDict.keys():
                new_color = colorActionDict[action]
                self.parent.artists[ident].artist.setPen(new_color, symbolBrush=new_color)
                self.changeTraceListColor(ident, new_color)

