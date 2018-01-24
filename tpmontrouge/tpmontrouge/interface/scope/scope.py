import pyqtgraph as pg
from time import sleep, time
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.widgets.MatplotlibWidget
import numpy as np
import os

from ..utils.start_stop_pause import ExpThread, StateMachine
from ..utils.start_stop_pause import StartStopPause


#from ...instrument.gbf.interface_qt import GBFConnection
from ...instrument.scope.interface_qt import ScopeConnection

from ...experiment.bode_plot import BodeExperiment as _BodeExperiment

from pyqtgraph.parametertree import Parameter, ParameterTree


class ScopeExperiment(object):
    def __init__(self, scope, scope_mpl_figure=None):
        self.scope = scope
        self.scope_mpl_figure = scope_mpl_figure
        self.mem = {}

    def loop(self, iterator, delay=.5):
        t0 = time()
        for _ in iterator:
            self.mem = {}
#####            self.scope._root.current_frequency = 1000 + np.random.rand()*100
#            self.scope_mpl_figure.clf()
            self.scope.stop_acquisition()
            for channel in self.scope.list_of_active_channel:
                wfm = channel.get_waveform()
#                wfm.plot_matplotlib(fig=self.scope_mpl_figure)
                self.mem[channel.key] = wfm
            self.scope.start_acquisition()            
            if self.scope_mpl_figure:
                self.scope_mpl_figure.clf()
                for i, key in enumerate(sorted(self.mem)):
                    self.mem[key].plot_matplotlib(fig=self.scope_mpl_figure)
                self.scope_mpl_figure.canvas.draw()
            t = time()
            if t<t0+delay:
                sleep(delay + t0 -t)
            t0 = time()

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
        np.savetxt(fname, tout, header='\t'.join(name), newline='\r\n')


#    def display_last_point(self, last_point):
#        super(BodeExperiment, self).display_last_point(last_point)
#        if self.scope_mpl_figure is not None:
#            fig = self.scope_mpl_figure
#            fig.clf()
#            last_point.plot(fig)
#            fig.canvas.draw()
#        if self.bode_mpl_figure is not None:
#            fig = self.bode_mpl_figure 
#            fig.clf()
#            self._bode_plot.plot(fig, log_scale=self.log_scale)
#            fig.canvas.draw()

class ScopeThread(ExpThread):
    def __init__(self, *args, scope_windows=None, **kwd):
        self.scope_windows = scope_windows
        kwd['btn'] = scope_windows.start_stop_buttons
        super().__init__(*args, **kwd)

    @property
    def scope(self):
        self.scope_windows.scope.auto_connect()
        return self.scope_windows.scope.device

    @property
    def exp(self):
        out = ScopeExperiment(self.scope, scope_mpl_figure=self.scope_windows.plot1.getFigure())
        return out

    def get_iterator(self):
        def infinite():
            while True:
                yield None
        return infinite()


class MyMPLWidget(pyqtgraph.widgets.MatplotlibWidget.MatplotlibWidget):
    def __init__(self, *args, **kwd):
        super(MyMPLWidget, self).__init__()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHeightForWidth(True)
        self.setSizePolicy(sizePolicy)

    def heightForWidth(self, width):
        return width * 0.7

class ScopeStartStopPause(StartStopPause):
    def start_thread(self):
        self._thread = ScopeThread(scope_windows=self.parent())
        self._thread.start()

class ScopeWindows(QtGui.QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QtGui.QHBoxLayout()
        self.setLayout(main_layout)
        btn_layout = QtGui.QVBoxLayout()

        main_layout.addLayout(btn_layout)
        buttons = ScopeStartStopPause(layout=btn_layout, parent=self)
        btn_layout.addStretch(1)

        self.scope = ScopeConnection()
        btn_layout.addWidget(self.scope.make_layout())
        btn_layout.addStretch(1)

        self.start_stop_buttons = buttons

        plot1 = MyMPLWidget()
        tmp_layout = QtGui.QVBoxLayout()
        tmp_layout.addWidget(plot1)
        tmp_layout.addStretch(1)
        main_layout.addLayout(tmp_layout)
        self.plot1 = plot1

        self.save_btn = pg.QtGui.QPushButton("Save data")
        self.save_btn.setEnabled(False)
        self.save_btn.clicked.connect(self.save_experiment)
        btn_layout.addWidget(self.save_btn)
        buttons.connect(self.new_state_save)

    @property
    def running_exp(self):
        return self.start_stop_buttons._thread.running_exp

    _initial_dir = os.getenv('HOME') or ''
    def save_experiment(self):
        file_name = QtGui.QFileDialog.getSaveFileName(self, 'Save file', 
                        self._initial_dir, "Data file (*.txt)")
        if isinstance(file_name, tuple): # depends on the version ...
            file_name = file_name[0]
#        print(file_name)
        if file_name:
            self.running_exp.save(file_name)


    def new_state_save(self, state):
        if state=='Running':
            self.save_btn.setEnabled(False)
        elif state=='Paused':
            self.save_btn.setEnabled(True)
        elif state=='Stopped':
            if self.running_exp is not None:
                self.save_btn.setEnabled(True)
            else:
                self.save_btn.setEnabled(False)



if __name__=='__main__':
    app = pg.QtGui.QApplication([])
    win = ScopeWindows()
    win.show()
    app.exec_()

