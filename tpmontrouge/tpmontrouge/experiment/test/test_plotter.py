import unittest
import tempfile
import os
from random import random

import matplotlib
matplotlib.use('Agg')
from matplotlib.pyplot import figure

from ..plotter import PlotterExperiment

import pyqtgraph as pg
import pyqtgraph.exporters
from ...interface.test.pyqt_graph_test_helper import PyQtPlotGraphicsTest, PyQtPlotGraphicsTestBis

#class BodePlotTest(PyQtPlotGraphicsTestBis):
#    def plot(self):
#        gbf = GBF(RootGBF())
#        scope = Scope(RootScope())

#        bode_experiment = BodeExperiment(gbf, scope, scope.channel2, scope.channel1, disp=False, wait_time=0)

#        bode_plot = bode_experiment.record_bode_diagramm(start=3, stop=3000, step=20, auto_set=True)
##        app_test = PyQtPlotGraphicsTest()
#        bode_plot.plot_pyqtgraph(self.view)
#        self.filename = os.path.join(tempfile.gettempdir(), 'bode_test_with_instrument.png')
##        app_test.exec_and_save(filename)

class DummyPlotterInterface(object):
    def __init__(self, name):
        self.name = name

    def get_one_point(self):
        return random()


int1 = DummyPlotterInterface('Interface 1')
int2 = DummyPlotterInterface('Interface 2')
int3 = DummyPlotterInterface('Interface 3')

class Test(unittest.TestCase):
    def testA(self):

        plotter_experiment = PlotterExperiment([int1], sample_rate=100000, disp=False)

        plotter_experiment.loop(range(10))
        fig = figure()
        plotter_experiment.plot_matplotlib(fig=fig)
        filename = os.path.join(tempfile.gettempdir(), 'plotter_experiment_testA.pdf')
        fig.savefig(filename)

        self.assertIn('Interface 1', plotter_experiment.last_points_as_str)

    def testB(self):

        plotter_experiment = PlotterExperiment([int1, int2, int3], sample_rate=100000, disp=False)

        plotter_experiment.loop(range(10))
        fig = figure()
        plotter_experiment.plot_matplotlib(fig=fig)
        filename = os.path.join(tempfile.gettempdir(), 'plotter_experiment_testB.pdf')
        fig.savefig(filename)

        self.assertIn('Interface 1', plotter_experiment.last_points_as_str)
        self.assertIn('Interface 2', plotter_experiment.last_points_as_str)


    def testC(self):
        BodePlotPyQTGraph(1).test()

    def testD(self):
        BodePlotPyQTGraph(3).test()


class BodePlotPyQTGraph(PyQtPlotGraphicsTestBis):
    def __init__(self, n):
        self._n = n
        super().__init__()
    def plot(self):
        
        if self._n ==1:
            plotter_experiment = PlotterExperiment([int1], sample_rate=100000, disp=False)
        else:
            plotter_experiment = PlotterExperiment([int1, int2, int3], sample_rate=100000, disp=False)
    

        plotter_experiment.loop(range(10))
        plotter_experiment.plot_pyqtgraph(view=self.view)
        self.filename = os.path.join(tempfile.gettempdir(), 'plotter_experiment_test_pyqt_{}.jpg'.format(self._n))
