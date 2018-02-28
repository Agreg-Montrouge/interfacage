from time import sleep

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

from ...experiment.plotter import PlotterExperiment as _PlotterExperiment
from ..utils.start_stop_pause import ExpThread
from ..utils.start_stop_pause import StartStopPauseSave


class PlotterExperiment(_PlotterExperiment):
    def __init__(self, list_of_interface, sample_rate, thread=None):
        super(PlotterExperiment, self).__init__(list_of_interface, sample_rate)
        self.thread = thread


class PlotterWindows(QtGui.QWidget):
    plotter_experiment = PlotterExperiment
    def __init__(self):
        super(PlotterWindows, self).__init__()
        self.main_layout = main_layout = QtGui.QHBoxLayout()
        self.setLayout(main_layout)
        btn_layout = QtGui.QVBoxLayout()

        main_layout.addLayout(btn_layout)

        self.start_stop_buttons = BodeStartStopPauseSave(layout=btn_layout, parent=self)



