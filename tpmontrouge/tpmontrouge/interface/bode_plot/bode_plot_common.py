import pyqtgraph as pg
from time import sleep
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.widgets.MatplotlibWidget
import numpy as np
import os

from ..utils.start_stop_pause import ExpThread, StateMachine
from ..utils.start_stop_pause import StartStopPauseSave


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
        self._last_point = last_point
#        self.thread.end_of_one_iteration.emit((last_point, self._bode_plot))

params = [{'name':'Start', 'type':'float', 'value':100, 'suffix': 'Hz', 'siPrefix': True, 'limits':(0, None), 'dec':True, 'step':.5}, 
            {'name':'Stop', 'type':'float', 'value':10000, 'suffix': 'Hz', 'siPrefix': True, 'limits':(0, None), 'dec':True, 'step':.5}, 
             {'name':'Step', 'type':'int', 'value':20, 'dec':True},
        {'name':'log', 'type':'bool', 'value':True},
        {'name':'Ref. chan.', 'type':'list', 'values':[1, 2, 3, 4], 'value':1},
        {'name':'Sig. chan.', 'type':'list', 'values':[1, 2, 3, 4], 'value':2},
]


class BodeStartStopPauseSave(StartStopPauseSave):
    def start_thread(self):
        self._thread = BodeThread(parent_windows=self.parent())
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
    def __init__(self, **kwd):
        super(BodeWindows, self).__init__(**kwd)
        self.main_layout = main_layout = QtGui.QHBoxLayout()
        self.setLayout(main_layout)
        btn_layout = QtGui.QVBoxLayout()

        main_layout.addLayout(btn_layout)

        self.start_stop_buttons = BodeStartStopPauseSave(layout=btn_layout, parent=self)


        p = Parameter.create(name='params', type='group', children=params)
        t = ParameterTree()
        t.setParameters(p, showTop=False)


        btn_layout.addWidget(t)
#        btn_layout.addStretch(1)

        self.add_plot_widgets()

        self.bode_params = p
        self.bode_params_tree = t

        self.gbf = GBFConnection()
        btn_layout.addWidget(self.gbf.make_layout())

        self.scope = ScopeConnection()
        btn_layout.addWidget(self.scope.make_layout())
        btn_layout.addStretch(1)
#        btn_layout.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)

        self.start_stop_buttons.connect(self.new_state_tree)
        self.start_stop_buttons.connect(self.parent().new_tab_state)

    @property
    def running_exp(self):
        return self.start_stop_buttons._thread.running_exp

    def new_state_tree(self, state):
        if state=='Running' or state=='Paused':
            self.bode_params_tree.setEnabled(False)
        else:
            self.bode_params_tree.setEnabled(True)

    def end_of_one_iteration(self, data):
        print('END OF ONE ITERATION', data)   

    def test_action(self):
        self.scope.choices.setCurrentIndex(self.scope.choices.count()-1)
        self.gbf.choices.setCurrentIndex(self.gbf.choices.count()-1)
        self.start_stop_buttons.on_off_btn.click()

class BodeThread(ExpThread):
    @property
    def parameters(self):
        return self.parent_windows.bode_params

    @property
    def gbf(self):
        self.parent_windows.gbf.auto_connect()
        return self.parent_windows.gbf.device

    @property
    def scope(self):
        self.parent_windows.scope.auto_connect()
        return self.parent_windows.scope.device

    @property
    def exp(self):
        return self.parent_windows.bode_experiment(self.gbf, self.scope, 
                                self.scope.channel[self.parameters['Sig. chan.']], 
                                self.scope.channel[self.parameters['Ref. chan.']], 
                                disp=True, wait_time=0,
                                scope_figure=self.parent_windows.plot1, 
                                bode_figure=self.parent_windows.plot2,
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

