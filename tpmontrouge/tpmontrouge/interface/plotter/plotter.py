from time import sleep

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

from ...experiment.plotter import PlotterExperiment as _PlotterExperiment
from ...experiment.test.test_plotter import int1, int2
from ..utils.start_stop_pause import ExpThread
from ..utils.start_stop_pause import StartStopPauseSave


from ...instrument.voltmeter.interface_qt import VoltmeterConnection

class PlotterExperiment(_PlotterExperiment):
    def __init__(self, list_of_interface, sample_rate, thread=None, **kwd):
        super(PlotterExperiment, self).__init__(list_of_interface, sample_rate, **kwd)
        self.thread = thread

#    def plot(self):
#        self.thread.end_of_one_iteration.emit(self.plot_pyqtgraph)

class PlotterStartStopPauseSave(StartStopPauseSave):
    def start_thread(self):
        self._thread = PlotterThread(parent_windows=self.parent())
        self._thread.start()

class PlotterWindow(QtGui.QWidget):
    experiment = PlotterExperiment
    def __init__(self):
        super(PlotterWindow, self).__init__()
        self.main_layout = main_layout = QtGui.QHBoxLayout()
        self.setLayout(main_layout)
        btn_layout = QtGui.QVBoxLayout()
        main_layout.addLayout(btn_layout)

        start_stop_save_layout = QtGui.QHBoxLayout()
        btn_layout.addLayout(start_stop_save_layout)

        self.start_stop_buttons = PlotterStartStopPauseSave(layout=start_stop_save_layout, parent=self)

# Ajouter le sample rate

        
        self.sample_rate = pg.SpinBox(value=10, dec=True, step=1, bounds=[0.01, 100])
        tmp = pg.LayoutWidget()
        tmp.addWidget(pg.QtGui.QLabel('Sample rate'), col=0)
        tmp.addWidget(self.sample_rate, col=1)
        btn_layout.addWidget(tmp)

        n = 4
        self.voltmeters = []
        for i in range(n):
            voltmeter = VoltmeterConnection(with_enable_button=True)
            if i<2:
                voltmeter.set_state('Unconnected')
            btn_layout.addWidget(voltmeter.make_layout())
            self.voltmeters.append(voltmeter)
        btn_layout.addStretch(1)


        self.add_plot_widgets()

    def add_plot_widgets(self):
        plot1 = pg.GraphicsView() 
        tmp_layout = QtGui.QVBoxLayout()
        tmp_layout.addWidget(plot1)
        tmp_layout.addStretch(1)
        self.main_layout.addLayout(tmp_layout)
        self.plot1 = plot1


    def end_of_one_iteration(self, plot_function):
        view = self.plot1            
        self.start_stop_buttons._thread.running_exp.plot_pyqtgraph(view)
        #plot_function(view)

    def test_action(self):
        self.start_stop_buttons.on_off_btn.click()



class PlotterThread(ExpThread):
    @property
    def inst_list(self):
        out = []
        for elm in self.parent_windows.voltmeters:
            if elm.is_enable:
                elm.auto_connect()
                out.append(elm.device)
        return out

    @property
    def exp(self):
        try:
            out = self.parent_windows.experiment(self.inst_list, sample_rate=self.parent_windows.sample_rate.value(), disp=False)
        except Exception as e:
            print(e)
            raise
        return out

    def get_iterator(self):
        def infinite():
            while True:
                yield None
        return infinite()

