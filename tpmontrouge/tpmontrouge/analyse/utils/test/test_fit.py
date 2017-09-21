import unittest


from ..fit import fit_sinusoid

import numpy as np

class Test(unittest.TestCase):
    def fit(self, with_initial_freq, phase=.2):
        t = np.linspace(0, 1, 101)
        freq = 4
        y = .4 + .6*np.sin(2*np.pi*freq*t + phase)
        if with_initial_freq:
            out = fit_sinusoid(t, y, freq=4.1)
        else:
            out = fit_sinusoid(t, y)
        self.assertAlmostEqual(out['phase'] if out['amplitude']>0 else (out['phase']+np.pi)%(2*np.pi), phase%(2*np.pi))
        self.assertAlmostEqual(out['frequency'], freq)
        self.assertAlmostEqual(out['offset'], .4)
        self.assertAlmostEqual(abs(out['amplitude']), 1.2)

    def test_fit(self):
        for phase in [0.1, .5, 1, 1.5, 2, 2.5, 3]:
            self.fit(True, phase=phase)
            self.fit(False, phase=phase)

