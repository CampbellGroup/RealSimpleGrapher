from PyQt5.QtWidgets import *
from twisted.internet.defer import inlineCallbacks


class ParameterList(QWidget):

    def __init__(self, dataset):
        super(ParameterList, self).__init__()
        self.dataset = dataset
        mainLayout = QVBoxLayout()
        self.parameterListWidget = QListWidget()
        mainLayout.addWidget(self.parameterListWidget)
        self.setWindowTitle(
            str(dataset.dataset_name)
        )  # + " " + str(dataset.directory))
        self.populate()
        self.setLayout(mainLayout)
        self.show()

    @inlineCallbacks
    def populate(self):
        parameters = yield self.dataset.get_parameters()
        self.parameterListWidget.clear()
        self.parameterListWidget.addItems([str(x) for x in sorted(parameters)])
