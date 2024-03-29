import pyqtgraph as pg
from time import sleep, time
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.widgets.MatplotlibWidget
import numpy as np
import os

from ..utils.start_stop_pause import ExpThread, StateMachine
from ..utils.start_stop_pause import StartStopPauseSaveSingle

from ...instrument.scope.interface_qt import ScopeConnection

from ...experiment.bode_plot import BodeExperiment as _BodeExperiment

from pyqtgraph.parametertree import Parameter, ParameterTree


class SingleType(object):
    pass

Single = SingleType()

class ScopeExperiment(object):
    def __init__(self, scope, scope_figure=None, thread=None):
        self.scope = scope
        self.scope_figure = scope_figure
        self.mem = {}
        self.thread = thread

    def loop(self, iterator, delay=None):
        if delay is None:
            delay = self.scope.horizontal.offset + 5*self.scope.horizontal.scale
            delay = max(delay, 0.5)
        t0 = time()
        for val in iterator:
            self.mem = {}
            for i in range(2):
                try:
                    if val is not Single:
                        self.scope.stop_after_acquisition()
                    for channel in self.scope.list_of_active_channel:
                        wfm = channel.get_waveform()
                        self.mem[channel.key] = wfm
                    if val is not Single:
                        self.scope.start_acquisition()            
                    break
                except Exception as e:
                    print('ERROR', e)
                    print('Try again')
                    if i==1:
                        raise e
            self.plot()
            t = time()
            sleep(0.2)
            if t<t0+delay:
                sleep(delay + t0 -t)
            t0 = time()

    def plot(self):
        self.thread.end_of_one_iteration.emit(self.mem.copy())

    def save(self, fname):
        if self.mem:
            for i, key in enumerate(sorted(self.mem)):
                wfm = self.mem[key]
                if i==0:
                    x = wfm.x_data
                    out = [x]
                    name = ['Time']
                y = wfm.y_data
                out += [y]
                name += ['CH{}'.format(key)]
        tout = np.array(out).T
        header = ' '.join(['{:25}'.format(elm) for elm in name])
        np.savetxt(fname, tout, header=header, newline='\r\n')


class ScopeThread(ExpThread):
    def __init__(self, single=False, **kwd):
        super(ScopeThread, self).__init__(**kwd)
        self._single = single

    @property
    def scope(self):
        self.parent_windows.scope.auto_connect()
        return self.parent_windows.scope.device

    @property
    def exp(self):
        out = self.parent_windows.experiment(self.scope, scope_figure=self.parent_windows.plot1, thread=self)
        return out

    def get_iterator(self):
        if self._single:
            return [Single]
        def infinite():
            while True:
                yield None
        return infinite()



class ScopeStartStopPauseSave(StartStopPauseSaveSingle):
    def start_thread(self):
        self._thread = ScopeThread(parent_windows=self.parent())
        self._thread.start()

    def start_single_thread(self):
        self._thread = ScopeThread(parent_windows=self.parent(), single=True)
        self._thread.start()

class ScopeWindows(QtGui.QWidget):
    experiment = ScopeExperiment
    def __init__(self, **kwd):
        super().__init__(**kwd)
        self.main_layout = main_layout = QtGui.QHBoxLayout()
        self.setLayout(main_layout)
        btn_layout = QtGui.QVBoxLayout()

        main_layout.addLayout(btn_layout)
        self.start_stop_buttons = ScopeStartStopPauseSave(layout=btn_layout, parent=self)
        btn_layout.addStretch(1)

        self.scope = ScopeConnection()
        btn_layout.addWidget(self.scope.make_layout())
        btn_layout.addStretch(1)

        self.add_plot_widgets()
        if self.parent():
            self.start_stop_buttons.connect(self.parent().new_tab_state)


    @property
    def running_exp(self):
        return self.start_stop_buttons._thread.running_exp


    def end_of_one_iteration(self, data):
        pass

    def test_action(self):
        self.scope.choices.setCurrentIndex(self.scope.choices.count()-1)
        self.start_stop_buttons.on_off_btn.click()

if __name__=='__main__':
    app = pg.QtGui.QApplication([])
    win = ScopeWindows()
    win.show()
    app.exec_()

