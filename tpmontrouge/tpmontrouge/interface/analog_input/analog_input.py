from time import sleep, time

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

from ...experiment.continuous_acquisition import AIExperiment as _AIExperiment
from ..utils.start_stop_pause import ExpThread
from ..utils.start_stop_pause import StartStopPauseSave


from ...instrument.analog_input.interface_qt import AIConnection

class AIExperiment(_AIExperiment):
    pass
#    def __init__(self, list_of_interface, sample_rate, thread=None, **kwd):
#        super(PlotterExperiment, self).__init__(list_of_interface, sample_rate, **kwd)
#        self.thread = thread

#    def plot(self):
#        self.thread.end_of_one_iteration.emit(self.plot_pyqtgraph)

class PlotterStartStopPauseSave(StartStopPauseSave):
    def start_thread(self):
        self._thread = AIThread(parent_windows=self.parent())
        self._thread.start()

class AIWindow(QtGui.QWidget):
    experiment = AIExperiment
    def __init__(self, **kwd):
        super(AIWindow, self).__init__(**kwd)
        self.main_layout = main_layout = QtGui.QHBoxLayout()
        self.setLayout(main_layout)
        btn_layout = QtGui.QVBoxLayout()
        main_layout.addLayout(btn_layout)

        start_stop_save_layout = QtGui.QHBoxLayout()
        btn_layout.addLayout(start_stop_save_layout)

        self.start_stop_buttons = PlotterStartStopPauseSave(layout=start_stop_save_layout, parent=self)

        self.sample_rate = pg.SpinBox(value=1000, step=1, dec=True, int=True, siPrefix=True, bounds=[1, 100000], suffix='S/s')
        tmp = pg.LayoutWidget()
        tmp.addWidget(pg.QtGui.QLabel('Sample rate'), col=0)
        tmp.addWidget(self.sample_rate, col=1)
        btn_layout.addWidget(tmp)

        self.duration = pg.SpinBox(value=10, dec=True, step=1, bounds=[1, 10000], suffix=' s')
        tmp = pg.LayoutWidget()
        tmp.addWidget(pg.QtGui.QLabel('Acquisition duration'), col=0)
        tmp.addWidget(self.duration, col=1)
        btn_layout.addWidget(tmp)

        ai = AIConnection(with_enable_button=False)
        btn_layout.addWidget(ai.make_layout())
        self.ai = ai

        self.channels = []
        self.channel_items = ["off", "0", "1", "2", "3"]
        for i in range(4):
            chan = pg.ComboBox(items = self.channel_items, default=self.channel_items[1] if i==0 else None)
            self.channels.append(chan)
            btn_layout.addWidget(chan)


        btn_layout.addStretch(1)

        self.add_plot_widgets()
        if self.parent():
            self.start_stop_buttons.connect(self.parent().new_tab_state)

    @property
    def channel_list(self):
        out = []
        for elm in self.channels:
            if elm.value()!='off':
                out.append(elm.value())
        return out

    def add_plot_widgets(self):
        plot1 = pg.GraphicsView()
        tmp_layout = QtGui.QVBoxLayout()
        tmp_layout.addWidget(plot1)
        tmp_layout.addStretch(1)
        self.main_layout.addLayout(tmp_layout)
        self.plot1 = plot1


    t0 = time()
    def end_of_one_iteration(self, plot_function):
        view = self.plot1
        t = time()
        if t>self.t0 + 0.5:
            self.start_stop_buttons._thread.running_exp.plot_pyqtgraph(view)
            self.t0 = t
        #plot_function(view)

    def test_action(self):
        self.start_stop_buttons.on_off_btn.click()



class AIThread(ExpThread):
    @property
    def ai(self):
        self.parent_windows.ai.auto_connect()
        return self.parent_windows.ai.device


    dt = 0.1

    @property
    def exp(self):
        try:
            out = self.parent_windows.experiment(self.ai, self.parent_windows.channel_list, sample_rate=self.parent_windows.sample_rate.value(), 
                                    block_size=int(self.parent_windows.sample_rate.value()*self.dt), N_block=self.N, disp=False)
        except Exception as e:
            print(e)
            raise
        return out

    @property
    def N(self):
        return int(self.parent_windows.duration.value()/self.dt)


    def get_iterator(self):
        return range(self.N)








