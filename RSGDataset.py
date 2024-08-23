"""
Parent class for datasets
"""
from twisted.internet.defer import inlineCallbacks, returnValue, DeferredLock
from PyQt5.QtCore import QObject

import numpy as np


class RSGDataset(QObject):

    def __init__(self, data_vault, context, dataset_location, reactor):
        super(RSGDataset, self).__init__()
        self.data = None
        self.accessingData = DeferredLock()
        self.reactor = reactor
        self.dataset_location = dataset_location
        self.data_vault = data_vault
        self.updateCounter = 0
        self.context = context
        self.dataset_name = None
        self.connect_datavault()
        self.setup_listeners()

    def connect_datavault(self):
        yield self.data_vault.cd(self.dataset_location[0], context=self.context)
        path, dataset_name = yield self.data_vault.open(self.dataset_location[1], context=self.context)
        self.dataset_name = dataset_name

    @inlineCallbacks
    def setup_listeners(self):
        yield self.data_vault.signal__data_available(11111, context=self.context)
        yield self.data_vault.addListener(listener=self.update_data, source=None, ID=11111, context=self.context)

    @inlineCallbacks
    def open_dataset(self):
        yield self.data_vault.cd(self.dataset_location[0], context=self.context)
        yield self.data_vault.open(self.dataset_location[1], context=self.context)

    @inlineCallbacks
    def get_parameters(self):
        parameters = yield self.data_vault.parameters(context=self.context)
        parameter_values = []
        for parameter in parameters:
            parameter_value = yield self.data_vault.get_parameter(parameter, context=self.context)
            parameter_values.append((parameter, parameter_value))
        returnValue(parameter_values)

    def update_data(self, x, y):
        self.updateCounter += 1
        self.get_data()

    @inlineCallbacks
    def get_data(self):
        from labrad.units import DimensionlessArray
        data = yield self.data_vault.get(100, context=self.context)
        if self.data is None:
            yield self.accessingData.acquire()
            if isinstance(data, DimensionlessArray):
                self.data = data
            else:
                self.data = data.asarray
            self.accessingData.release()
        else:
            yield self.accessingData.acquire()
            if isinstance(data, DimensionlessArray):
                self.data = np.append(self.data, data, 0)
            else:
                self.data = np.append(self.data, data.asarray, 0)
            self.accessingData.release()

    @inlineCallbacks
    def get_labels(self):
        labels = []
        yield self.open_dataset()
        variables = yield self.data_vault.variables(context=self.context)
        path, dataset_name = yield self.data_vault.open(self.dataset_location[1], context=self.context)
        for i in range(len(variables[1])):
            labels.append(variables[1][i][1] + ' - ' + dataset_name)
        returnValue(labels)

    @inlineCallbacks
    def disconnect_data_signal(self):
        yield self.data_vault.removeListener(listener=self.update_data, source=None, ID=11111, context=self.context)
