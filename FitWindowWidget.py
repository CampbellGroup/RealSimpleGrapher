from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *

from twisted.internet.defer import inlineCallbacks, returnValue, DeferredLock, Deferred
from analysis.fitting import FitWrapper
from queue import Queue


class RowInfo:
    """
    Container for the widgets with
    each row in the parameters table
    """

    def __init__(self, vary, manual_value, fitted_value):
        self.vary_select = vary
        self.manual_value = manual_value
        self.fitted_value = fitted_value


class FitWindow(QWidget):

    def __init__(self, dataset, index, parent):
        super(FitWindow, self).__init__()
        self.dataset = dataset
        self.index = index
        self.parent = parent
        self.fw = FitWrapper(dataset, index)
        self.row_info_dict = {}
        self.ident = "Fit: " + str(self.dataset.dataset_name)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.ident)
        main_layout = QVBoxLayout()
        buttons = QHBoxLayout()

        self.model_select = QComboBox(self)
        for model in self.fw.models:
            self.model_select.addItem(model)

        self.parameterTable = QTableWidget()
        self.parameterTable.setColumnCount(4)

        self.fitButton = QPushButton("Fit", self)

        self.plotButton = QPushButton("Plot manual", self)

        self.fw.setModel(str(self.model_select.currentText()))

        main_layout.addWidget(self.model_select)
        main_layout.addWidget(self.parameterTable)
        main_layout.addLayout(buttons)
        buttons.addWidget(self.fitButton)
        buttons.addWidget(self.plotButton)

        self.model_select.activated.connect(self.onActivated)
        self.fitButton.clicked.connect(self.onClick)
        self.plotButton.clicked.connect(self.onPlot)

        self.setupParameterTable()
        self.setLayout(main_layout)
        self.show()

    def setupParameterTable(self):

        self.parameterTable.clear()

        header_labels = ["Vary", "Param", "Manual", "Fitted"]
        self.parameterTable.setHorizontalHeaderLabels(header_labels)
        self.parameterTable.horizontalHeader().setStretchLastSection(True)

        params = self.fw.getParameters()
        self.parameterTable.setRowCount(len(params))
        for i, p in enumerate(params):

            vary_select = QTableWidgetItem()
            label = QLabel(p)
            manual_value = QDoubleSpinBox()
            fitted_value = QTableWidgetItem()

            self.row_info_dict[p] = RowInfo(vary_select, manual_value, fitted_value)

            vary_select.setFlags(
                QtCore.Qt.ItemFlag.ItemIsUserCheckable
                | QtCore.Qt.ItemFlag.ItemIsEnabled
            )
            if self.fw.getVary(p):
                vary_select.setCheckState(QtCore.Qt.CheckState.Checked)
            else:
                vary_select.setCheckState(QtCore.Qt.CheckState.Unchecked)

            manualValue = self.fw.getManualValue(p)
            manual_value.setDecimals(6)
            manual_value.setRange(-1000000000, 1000000000)
            manual_value.setValue(manualValue)

            fittedValue = self.fw.getFittedValue(p)
            # fitted_value.setDecimals(6)
            # fitted_value.setRange(-1000000000, 1000000000)
            fitted_value.setText(str(fittedValue))
            self.parameterTable.setItem(i, 0, vary_select)
            self.parameterTable.setCellWidget(i, 1, label)
            self.parameterTable.setCellWidget(i, 2, manual_value)
            self.parameterTable.setItem(i, 3, fitted_value)

    def updateParametersToFitter(self):
        params = self.fw.getParameters()
        for p in params:
            row = self.row_info_dict[p]
            vary = row.vary_select.checkState()
            manual_value = row.manual_value.value()
            if vary:
                self.fw.setVary(p, True)
            else:
                self.fw.setVary(p, False)
            self.fw.setManualValue(p, manual_value)

    def updateParametersFromFitter(self):
        """
        Set the fitted and manual parameters
        fields to the fit values
        """
        params = self.fw.getParameters()
        for p in params:
            row = self.row_info_dict[p]
            fitted_value = self.fw.getFittedValue(p)
            row.fitted_value.setText(str(fitted_value))
            row.manual_value.setValue(fitted_value)

    def plotFit(self):
        """
        Plot the fitted parameters.
        We need to wrap the data in a dataset
        object to use add_artist in GraphWidget
        """

        class dataset:
            def __init__(self, data):
                self.data = data
                self.updateCounter = 1

        data = self.fw.evaluateFittedParameters()
        ds = dataset(data)
        try:
            # remove the previous fit
            self.parent.parent.remove_artist(self.ident)
            self.parent.parent.add_artist(self.ident, ds, 0, no_points=True)
        except:
            self.parent.parent.add_artist(self.ident, ds, 0, no_points=True)

    def onActivated(self):
        """
        Run when model is changed.
        Reset row_info_dict each
        time the model is changed.
        """
        model = str(self.model_select.currentText())
        self.fw.setModel(model)
        self.row_info_dict = {}
        self.setupParameterTable()

    def onClick(self):
        """
        Send table parameters to fitter,
        perform fit, and then update
        paramter table with the results
        """

        self.updateParametersToFitter()
        self.fw.doFit()
        self.updateParametersFromFitter()
        self.plotFit()

    def onPlot(self):
        """
        Plot the manual parameters. See documentation
        for plotFit()
        """

        class dataset:
            def __init__(self, data):
                self.data = data
                self.updateCounter = 1

        self.updateParametersToFitter()
        data = self.fw.evaluateManualParameters()
        ds = dataset(data)
        try:
            # remove the previous plot
            self.parent.parent.remove_artist(self.ident)
            self.parent.parent.add_artist(self.ident, ds, 0, no_points=True)
        except:
            self.parent.parent.add_artist(self.ident, ds, 0, no_points=True)

    def closeEvent(self, event):
        self.parent.parent.remove_artist(self.ident)
