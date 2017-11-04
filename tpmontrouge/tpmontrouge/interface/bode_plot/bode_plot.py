import pyqtgraph as pg
from time import sleep
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.widgets.MatplotlibWidget
import numpy as np

from ..utils.start_stop_pause import ExpThread, StateMachine
from ..utils.start_stop_pause import StartStopPause

from ...experiment.test.virtual_instrument_for_bode_plot import RootGBF, RootScope
from ...instrument.gbf.gbf import GBF
from ...instrument.scope.scope import Scope
from ...experiment.bode_plot import BodeExperiment as _BodeExperiment

app = pg.QtGui.QApplication([])

from pyqtgraph.parametertree import Parameter, ParameterTree

#gbf = GBF(RootGBF())
#scope = Scope(RootScope())

class BodeExperiment(_BodeExperiment):
    def __init__(self, *args, scope_mpl_figure=None, bode_mpl_figure=None, **kwd):
        self.scope_mpl_figure = scope_mpl_figure
        self.bode_mpl_figure = bode_mpl_figure
        super(BodeExperiment, self).__init__(*args, **kwd)

    def loop(self, iterator):
        self.record_bode_diagramm(list_of_frequency=iterator)

    def display_last_point(self, last_point):
        super(BodeExperiment, self).display_last_point(last_point)
        if self.scope_mpl_figure is not None:
            fig = self.scope_mpl_figure
            fig.clf()
            last_point.plot(fig)
            fig.canvas.draw()
        if self.bode_mpl_figure is not None:
            fig = self.bode_mpl_figure 
            fig.clf()
            self._bode_plot.plot(fig)
            fig.canvas.draw()

params = [{'name':'Start', 'type':'float', 'value':100, 'suffix': 'Hz', 'siPrefix': True, 'limits':(0, None), 'dec':True, 'step':.5}, 
            {'name':'Stop', 'type':'float', 'value':10000, 'suffix': 'Hz', 'siPrefix': True, 'limits':(0, None), 'dec':True, 'step':.5}, 
             {'name':'Step', 'type':'int', 'value':20, 'dec':True},
        {'name':'log', 'type':'bool', 'value':True}]


class BodeStartStopPause(StartStopPause):
    def start_thread(self):
        self._thread = BodeThread(bode_windows=self.parent())
        self._thread.start()

class Connection(StateMachine):
    name = ""
    _device = None
    def __init__(self, *args, **kwd):
        super(Connection, self).__init__(states=['Unconnected', 'Connected'], *args, **kwd)

        self.button = pg.QtGui.QPushButton("")
        self.choices = pg.QtGui.QComboBox()
        self.choices.addItems([])

        self.entering_unconnected()
        self.button.clicked.connect(self.connect_button_pressed)

        self.refresh_btn = QtGui.QPushButton("Reload")
#        self.refresh_btn.setFixedWidth(20)
#        self.refresh_btn.setFixedHeight(20)
#        self.refresh_btn.setIcon(QtGui.QIcon(pixmaps.getPixmap('default')))
        self.refresh_btn.clicked.connect(self.refresh)  
        self.refresh()


    def connect_button_pressed(self):
        if self.state=='Connected':
            self.set_state('Unconnected')
        elif self.state=='Unconnected':
            self.set_state('Connected')

    def entering_connected(self, previous_state=None):
        self.choices.setEnabled(False)
        self.button.setText('Disconnect')
        self.create_device()

    def entering_unconnected(self, previous_state=None):
        self.choices.setEnabled(True)
        self.button.setText('Connect')

    def make_layout(self):
        layout = pg.LayoutWidget()
        label = pg.QtGui.QLabel()
        label.setText(self.name)
        layout.addWidget(label, colspan=2)
        layout.addWidget(self.button, row=1, col=0)
        layout.addWidget(self.choices, row=1, col=1)
        layout.addWidget(self.refresh_btn, row=1, col=2)
        return layout

    def refresh(self):
        self.choices.clear()
        list_of_device = self.get_list_of_devices()
#        self.choices.addItem('Default')
#        self.choices.insertSeparator(10000)
        self.choices.addItems(list_of_device)
        self.choices.insertSeparator(10000)
        self.choices.addItem('Simulation')

    def auto_connect(self):
        if self.get_state()=='Unconnected':
            self.entering_connected()
            self.set_state('Connected')        

    @property
    def device(self):
        device = self._device
        if device is None:
            raise Exception('No device connected')
        return device

from ...instrument.gbf import gbf_factory, get_all_gbf
from ...instrument.scope import scope_factory,get_all_scopes

class GBFConnection(Connection):
    name = 'GBF'
    default = 'Simulation'

    def get_list_of_devices(self):
        return get_all_gbf()

    def create_device(self):
        value = self.choices.currentText()
        if value=="Default":
            value = self.default
        if value=='Simulation':
            self._device = GBF(RootGBF())
        else:
            self._device = gbf_factory(value)

class ScopeConnection(Connection):
    name = 'Scope'
    default = 'Simulation'

    def get_list_of_devices(self):
        return get_all_scopes()

    def create_device(self):
        value = self.choices.currentText()
        if value=="Default":
            value = self.default
        if value=='Simulation':
            self._device = Scope(RootScope())
        else:
            self._device = scope_factory(value)

class BodeWindows(QtGui.QWidget):
    def __init__(self):
        super(BodeWindows, self).__init__()
        main_layout = QtGui.QHBoxLayout()
        self.setLayout(main_layout)
        btn_layout = QtGui.QVBoxLayout()

        main_layout.addLayout(btn_layout)

        p = Parameter.create(name='params', type='group', children=params)
        t = ParameterTree()
        t.setParameters(p, showTop=False)

        buttons = BodeStartStopPause(layout=btn_layout, parent=self)
        btn_layout.addWidget(t)
        btn_layout.addStretch(1)

        plot1 = pyqtgraph.widgets.MatplotlibWidget.MatplotlibWidget()
        main_layout.addWidget(plot1)
        plot2 = pyqtgraph.widgets.MatplotlibWidget.MatplotlibWidget()
        main_layout.addWidget(plot2)

        self.plot1 = plot1
        self.plot2 = plot2
        self.start_stop_buttons = buttons
        self.bode_params = p
        self.bode_params_tree = t

        self.gbf = GBFConnection()
        btn_layout.addWidget(self.gbf.make_layout())

        self.scope = ScopeConnection()
        btn_layout.addWidget(self.scope.make_layout())

        buttons.connect(self.new_state)


    def new_state(self, state):
        if state=='Running' or state=='Paused':
            self.bode_params_tree.setEnabled(False)
        else:
            self.bode_params_tree.setEnabled(True)

class BodeThread(ExpThread):
    def __init__(self, *args, bode_windows=None, **kwd):
        self.bode_windows = bode_windows
        kwd['btn'] = bode_windows.start_stop_buttons
        super(BodeThread, self).__init__(*args, **kwd)

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
        return BodeExperiment(self.gbf, self.scope, self.scope.channel1, self.scope.channel2, 
                                disp=True, wait_time=0,
                                scope_mpl_figure=self.bode_windows.plot1.getFigure(), 
                                bode_mpl_figure=self.bode_windows.plot2.getFigure())

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
    win = BodeWindows()
    win.show()
    app.exec_()

