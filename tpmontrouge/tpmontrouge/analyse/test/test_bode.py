import unittest
import os
import tempfile

import matplotlib
matplotlib.use('Agg')
from matplotlib.pyplot import figure
import numpy as np
from scipy import signal

from ..Bode import BodePoint, BodePlot


def generate_signal(freq):
    t = np.linspace(0, 1, 10001)
    ref = np.sin(2*np.pi*freq*t)
    b,a = signal.butter(1, [0.002, 0.004], btype='pass')
    out = signal.lfilter(b,a,ref)
    b,a = signal.butter(1, [0.02, 0.04], btype='pass')
    out = signal.lfilter(b,a,out)
    return t, ref, out


class Test(unittest.TestCase):
    def fit(self, phase=.2):
        t = np.linspace(0, 1, 101)
        freq = 4
        y1 = .6*np.sin(2*np.pi*freq*t + phase)
        y2 = .3*np.sin(2*np.pi*freq*t)
        bode_p = BodePoint(t, y1, y2, freq=freq)
        self.assertAlmostEqual(bode_p.delta_phi, phase)

    def test_fit(self):
        self.fit()

    def test_bode_plot(self):
        bode_plot = BodePlot('Filtre double')
        for freq in np.logspace(0.5, 3.5, 51):
            t, ref, out = generate_signal(freq)
            bode_plot.append(BodePoint(t, out, ref, freq=freq))
#        print(bode_plot.delta_phi)
#        print(bode_plot.gain)

        fig = figure()
        bode_plot.plot(fig=fig)
        fig.savefig(os.path.join(tempfile.gettempdir(), 'bode_test.pdf'))


