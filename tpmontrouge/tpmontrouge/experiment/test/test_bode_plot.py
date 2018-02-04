import unittest
import tempfile
import os


import matplotlib
matplotlib.use('Agg')
from matplotlib.pyplot import figure

from ..bode_plot import BodeExperiment

from ...instrument.gbf.gbf import GBF
from ...instrument.scope.scope import Scope

from .virtual_instrument_for_bode_plot import RootGBF, RootScope

import pyqtgraph as pg
import pyqtgraph.exporters
from ...interface.test.pyqt_graph_test_helper import PyQtPlotGraphicsTest




class Test(unittest.TestCase):
    def test(self):
        gbf = GBF(RootGBF())
        scope = Scope(RootScope())

        bode_experiment = BodeExperiment(gbf, scope, scope.channel2, scope.channel1, disp=False, wait_time=0)

        bode_plot = bode_experiment.record_bode_diagramm(start=3, stop=3000, step=20, auto_set=True)
        fig = figure()
        bode_plot.plot(fig=fig)
        filename = os.path.join(tempfile.gettempdir(), 'bode_test_with_instrument.pdf')
#        print('File written to ', filename)
        fig.savefig(filename)


    def test(self):
        gbf = GBF(RootGBF())
        scope = Scope(RootScope())

        bode_experiment = BodeExperiment(gbf, scope, scope.channel2, scope.channel1, disp=False, wait_time=0)

        bode_plot = bode_experiment.record_bode_diagramm(start=3, stop=3000, step=20, auto_set=True)
#        fig = figure()
        app_test = PyQtPlotGraphicsTest()
        bode_plot.plot_pyqtgraph(app_test.view)
        filename = os.path.join(tempfile.gettempdir(), 'bode_test_with_instrument.png')
        app_test.exec_and_save(filename)

        

