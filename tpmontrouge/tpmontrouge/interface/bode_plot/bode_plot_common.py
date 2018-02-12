import pyqtgraph as pg
from time import sleep
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.widgets.MatplotlibWidget
import numpy as np
import os

from ..utils.start_stop_pause import ExpThread, StateMachine
from ..utils.start_stop_pause import StartStopPause


from ...instrument.gbf.interface_qt import GBFConnection
from ...instrument.scope.interface_qt import ScopeConnection

from ...experiment.bode_plot import BodeExperiment as _BodeExperiment

from pyqtgraph.parametertree import Parameter, ParameterTree

#gbf = GBF(RootGBF())
#scope = Scope(RootScope())

class BodeExperiment(_BodeExperiment):
    def __init__(self, *args, log_scale=True, scope_figure=None, bode_figure=None, thread=None, **kwd):
        self.scope_figure = scope_figure
        self.bode_figure = bode_figure
        self.log_scale = log_scale
        self.thread = thread
        super(BodeExperiment, self).__init__(*args, **kwd)

    def loop(self, iterator):
        self.record_bode_diagramm(list_of_frequency=iterator)

    def display_last_point(self, last_point):
        super(BodeExperiment, self).display_last_point(last_point)
        self.thread.end_of_one_iteration.emit((last_point, self._bode_plot))
#        if self.scope_figure is not None:
#            fig = self.scope_figure
#            fig.clf()
#            last_point.plot(fig)
#            fig.canvas.draw()
#        if self.bode_figure is not None:
#            fig = self.bode_mpl_figure 
#            fig.clf()
#            self._bode_plot.plot(fig, log_scale=self.log_scale)
#            fig.canvas.draw()

params = [{'name':'Start', 'type':'float', 'value':100, 'suffix': 'Hz', 'siPrefix': True, 'limits':(0, None), 'dec':True, 'step':.5}, 
            {'name':'Stop', 'type':'float', 'value':10000, 'suffix': 'Hz', 'siPrefix': True, 'limits':(0, None), 'dec':True, 'step':.5}, 
             {'name':'Step', 'type':'int', 'value':20, 'dec':True},
        {'name':'log', 'type':'bool', 'value':True},
        {'name':'Ref. chan.', 'type':'list', 'values':[1, 2, 3, 4], 'value':1},
        {'name':'Sig. chan.', 'type':'list', 'values':[1, 2, 3, 4], 'value':2},
]


class BodeStartStopPause(StartStopPause):
    def start_thread(self):
        self._thread = BodeThread(bode_windows=self.parent())
        self._thread.start()


class MyMPLWidget(pyqtgraph.widgets.MatplotlibWidget.MatplotlibWidget):
    def __init__(self, *args, **kwd):
        super(MyMPLWidget, self).__init__()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHeightForWidth(True)
        self.setSizePolicy(sizePolicy)

    def heightForWidth(self, width):
        return width * 0.7

class BodeWindows(QtGui.QWidget):
    bode_experiment = BodeExperiment
    def __init__(self):
        super(BodeWindows, self).__init__()
        self.main_layout = main_layout = QtGui.QHBoxLayout()
        self.setLayout(main_layout)
        btn_layout = QtGui.QVBoxLayout()

        main_layout.addLayout(btn_layout)

        p = Parameter.create(name='params', type='group', children=params)
        t = ParameterTree()
        t.setParameters(p, showTop=False)

        buttons = BodeStartStopPause(layout=btn_layout, parent=self)
        self.start_stop_btns = buttons
        btn_layout.addWidget(t)
#        btn_layout.addStretch(1)

        self.add_plot_widgets()

        self.start_stop_buttons = buttons
        self.bode_params = p
        self.bode_params_tree = t

        self.gbf = GBFConnection()
        btn_layout.addWidget(self.gbf.make_layout())

        self.scope = ScopeConnection()
        btn_layout.addWidget(self.scope.make_layout())
        btn_layout.addStretch(1)
#        btn_layout.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)

        buttons.connect(self.new_state_tree)

        self.save_btn = pg.QtGui.QPushButton("Save data")
        self.save_btn.setEnabled(False)
        self.save_btn.clicked.connect(self.save_experiment)
        btn_layout.addWidget(self.save_btn)
        buttons.connect(self.new_state_save)


#    def add_plot_widgets(self):
#        plot1 = MyMPLWidget()
#        tmp_layout = QtGui.QVBoxLayout()
#        tmp_layout.addWidget(plot1)
#        tmp_layout.addStretch(1)
#        main_layout.addLayout(tmp_layout)
#        plot2 = MyMPLWidget()
#        tmp_layout = QtGui.QVBoxLayout()
#        tmp_layout.addWidget(plot2)
#        tmp_layout.addStretch(1)
#        main_layout.addLayout(tmp_layout)

#        self.plot1 = plot1
#        self.plot2 = plot2


    _initial_dir = os.getenv('HOME') or ''
    def save_experiment(self):
        file_name = QtGui.QFileDialog.getSaveFileName(self, 'Save file', 
                        self._initial_dir, "Data file (*.txt)")
        if isinstance(file_name, tuple): # depends on the version ...
            file_name = file_name[0]
        print(file_name)
        if file_name:
            self.running_exp.save(file_name)

    @property
    def running_exp(self):
        return self.start_stop_btns._thread.running_exp

    def new_state_tree(self, state):
        if state=='Running' or state=='Paused':
            self.bode_params_tree.setEnabled(False)
        else:
            self.bode_params_tree.setEnabled(True)


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

    def end_of_one_iteration(self, data):
        print('END OF ONE ITERATION', data)   


class BodeThread(ExpThread):
    end_of_one_iteration = pg.QtCore.Signal(object)
    def __init__(self, *args, bode_windows=None, **kwd):
        self.bode_windows = bode_windows
        kwd['btn'] = bode_windows.start_stop_buttons
        super(BodeThread, self).__init__(*args, **kwd)
        self.end_of_one_iteration.connect(bode_windows.end_of_one_iteration)

    @property
    def parameters(self):
        return self.bode_windows.bode_params

    @property
    def gbf(self):
        self.bode_windows.gbf.auto_connect()
        return self.bode_windows.gbf.device

    @property
    def scope(self):
        self.bode_windows.scope.auto_connect()
        return self.bode_windows.scope.device

    @property
    def exp(self):
        return self.bode_windows.bode_experiment(self.gbf, self.scope, 
                                self.scope.channel[self.parameters['Sig. chan.']], 
                                self.scope.channel[self.parameters['Ref. chan.']], 
                                disp=True, wait_time=0,
                                scope_figure=self.bode_windows.plot1, 
                                bode_figure=self.bode_windows.plot2,
                                log_scale = self.parameters['log'], thread=self)

    def get_iterator(self):
        p = self.parameters
        vals = p.value()
        start = p['Start']
        stop = p['Stop']
        step = p['Step']
        log = p['log']
        if log:
            return list(np.exp(np.linspace(np.log(start), np.log(stop), step, endpoint=False)))
        else:
            return list(np.linspace(start, stop, step, endpoint=False))

if __name__=='__main__':
    app = pg.QtGui.QApplication([])
    win = BodeWindows()
    win.show()
    app.exec_()

