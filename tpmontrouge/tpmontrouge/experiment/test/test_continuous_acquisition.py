import unittest
import tempfile
import os

import matplotlib
matplotlib.use('Agg')
from matplotlib.pyplot import figure

from ..continuous_acquisition import AIExperiment

import pyqtgraph as pg
import pyqtgraph.exporters
from ...interface.test.pyqt_graph_test_helper import PyQtPlotGraphicsTest, PyQtPlotGraphicsTestBis

from ...instrument.analog_input.test.simu_ai import AnalogInputThreadSimulation

#interf = AIInterface('test')
interf_thread = AnalogInputThreadSimulation('test')


class Test(unittest.TestCase):
    def testA(self):
        ai_experiment = AIExperiment(interf_thread, ['chA'], sample_rate=100000, block_size=10000, N_block=10, disp=False)
        ai_experiment.loop()

#        print(ai_experiment._acquisition_line.data)
        self.assertEqual(len(ai_experiment._acquisition_lines['chA'].data), 100000)

#class _Test():
#    def testA(self):

#        plotter_experiment = PlotterExperiment([int1], sample_rate=100000, disp=False)

#        plotter_experiment.loop(range(10))
#        fig = figure()
#        plotter_experiment.plot_matplotlib(fig=fig)
#        filename = os.path.join(tempfile.gettempdir(), 'plotter_experiment_testA.pdf')
#        fig.savefig(filename)

#        self.assertIn('Interface 1', plotter_experiment.last_points_as_str)

#    def testB(self):

#        plotter_experiment = PlotterExperiment([int1, int2, int3], sample_rate=100000, disp=False)

#        plotter_experiment.loop(range(10))
#        fig = figure()
#        plotter_experiment.plot_matplotlib(fig=fig)
#        filename = os.path.join(tempfile.gettempdir(), 'plotter_experiment_testB.pdf')
#        fig.savefig(filename)

#        self.assertIn('Interface 1', plotter_experiment.last_points_as_str)
#        self.assertIn('Interface 2', plotter_experiment.last_points_as_str)

#    def testC(self):
#        BodePlotPyQTGraph(1).test()

#    def testD(self):
#        BodePlotPyQTGraph(3).test()

#    def testE(self):

#        plotter_experiment = PlotterExperiment([int1, int2, int3], sample_rate=100000, disp=False)

#        plotter_experiment.loop(range(10))
#        filename = os.path.join(tempfile.gettempdir(), 'plotter_save.txt')
#        plotter_experiment.save(filename)


#class BodePlotPyQTGraph(PyQtPlotGraphicsTestBis):
#    def __init__(self, n):
#        self._n = n
#        super().__init__()
#    def plot(self):
#        
#        if self._n ==1:
#            plotter_experiment = PlotterExperiment([int1], sample_rate=100000, disp=False)
#        else:
#            plotter_experiment = PlotterExperiment([int1, int2, int3], sample_rate=100000, disp=False)
#    

#        plotter_experiment.loop(range(10))
#        plotter_experiment.plot_pyqtgraph(view=self.view)
#        self.filename = os.path.join(tempfile.gettempdir(), 'plotter_experiment_test_pyqt_{}.jpg'.format(self._n))

