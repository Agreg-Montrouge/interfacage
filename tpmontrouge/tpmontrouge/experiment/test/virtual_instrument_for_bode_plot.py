import numpy as np
from scipy import signal

from ...instrument.gbf.test.simu_gbf import GBFSimulation
from ...instrument.scope.test.simu_scope import ScopeSimulation
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
    _channel_state = {1:1, 2:1}
    current_frequency = None
    def get_channel_waveform(self, channel=None, **kwd):
        dt = 1E-5
        N = 100000
        freq = self.current_frequency
        if freq is None:
            freq = 1000 + np.random.rand()*100
        t0 = -dt*N/2
        Tt = (np.arange(N))*dt + t0
        _, ref, out = generate_signal(freq, Tt)
        number_of_cycle = 1000*dt*freq
        while number_of_cycle<5:
            dt *=10
            out = out[::10]
            ref = ref[::10]
            number_of_cycle = 1000*dt*freq
        sl = slice(None) if len(out)<1000 else slice(-1000,None)
        if channel==2:
            return Waveform(data=out[sl], t0=t0, dt=dt) 
        if channel==1:
            return Waveform(data=ref[sl], t0=t0, dt=dt) 

