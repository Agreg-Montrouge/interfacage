import unittest
import tempfile
import os

import numpy as np
from scipy import signal
import matplotlib
matplotlib.use('Agg')
from matplotlib.pyplot import figure

from ..bode_plot import BodeExperiment

from ...instrument.gbf.test.simu_gbf import GBFSimulation
from ...instrument.gbf.gbf import GBF
from ...instrument.scope.test.simu_scope import ScopeSimulation
from ...instrument.scope.scope import Scope
from ...instrument.scope.waveform import Waveform

def generate_signal(freq, Tt):
    dt = Tt[1] - Tt[0]
    ref = np.sin(2*np.pi*freq*Tt)
    b,a = signal.butter(1, [0.002, 0.004], btype='pass')
    out = signal.lfilter(b,a,ref)
    return Tt, ref, out


class RootGBF(GBFSimulation):
    def set_frequency(self, val):
        self._frequency = val
        RootScope.current_frequency = val

class RootScope(ScopeSimulation):
    def get_channel_waveform(self, channel=None, **kwd):
        dt = 1E-5
        N = 100000
        freq = self.current_frequency
        t0 = -dt*N/2
        Tt = (np.arange(N))*dt + t0
        _, ref, out = generate_signal(freq, Tt)
        number_of_cycle = 10000*dt*freq
        while number_of_cycle<20:
            dt *=10
            out = out[::10]
            ref = ref[::10]
            number_of_cycle = 10000*dt*freq
        sl = slice(None) if len(out)<10000 else slice(-10000,None)
        if channel==1:
            return Waveform(data=out[sl], t0=t0, dt=dt) 
        if channel==2:
            return Waveform(data=ref[sl], t0=t0, dt=dt) 

class Test(unittest.TestCase):
    def test(self):
        gbf = GBF(RootGBF())
        scope = Scope(RootScope())

        bode_experiment = BodeExperiment(gbf, scope, scope.channel1, scope.channel2, disp=False)

        bode_plot = bode_experiment.record_bode_diagramm(start=3, stop=3000, step=20)
        fig = figure()
        bode_plot.plot(fig=fig)
        filename = os.path.join(tempfile.gettempdir(), 'bode_test_with_instrument.pdf')
        print('File writte to ', filename)
        fig.savefig(filename)

        

