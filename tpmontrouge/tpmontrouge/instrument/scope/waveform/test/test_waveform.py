import unittest
import os
import tempfile

import numpy as np


import matplotlib
matplotlib.use('Agg')
from matplotlib.pyplot import figure

import pyqtgraph as pg
#pg.setConfigOption('background', 'w')
#pg.setConfigOption('foreground', 'k')
import pyqtgraph.exporters


from ..waveform import Waveform
from .....interface.test.pyqt_graph_test_helper import PyQtPlotGraphicsTestBis


dt = 1E-6
N = 10000
freq = 1000

data = np.sin(np.arange(N)*dt*2*np.pi*freq)
wf = Waveform(data = data, t0=0, dt=dt)

class WaveFormPyQtGraph(PyQtPlotGraphicsTestBis):
    def plot(self):
        wf.plot_matplotlib(self.view)
        self.filename = os.path.join(tempfile.gettempdir(), 'scope_test.jpg')




class TestWaveform(unittest.TestCase):
    def test_waveform(self):
        self.assertEqual(wf.N, N)
        self.assertEqual(wf.x_data[0], 0)
        self.assertEqual(wf.y_data[N//2], data[N//2])

    def test_plot_mpl(self):
        # Should be moved to test_waveform
        fig = figure()
        wf.plot_matplotlib(fig=fig)
        file = os.path.join(tempfile.gettempdir(), 'scope_test.pdf')
#        print('Figure saved to ', file)
        fig.savefig(file)


#    def test_plot_pyqtgraph(self):
#        plt = wf.plot_pyqtgraph()
#        exporter = pg.exporters.ImageExporter(plt.plotItem)
#        exporter.params.param('width').setValue(1920, blockSignal=exporter.widthChanged)
#        exporter.params.param('height').setValue(1080, blockSignal=exporter.heightChanged)
#        exporter.export(os.path.join(tempfile.gettempdir(), 'scope_test.png'))
