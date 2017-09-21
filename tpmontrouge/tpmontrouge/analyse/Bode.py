from cached_property import cached_property
from .utils.fit import fit_sinusoid
from .utils import unwrap_phase

import numpy as np

class BodePlot(object):
    title = None
    def __init__(self, title=None):
        if title is not None:
            self.title = title
        self._list_of_point = []


    def append(self, val):
        assert isinstance(val, BodePoint)
        self._list_of_point.append(val)


    def get_column(self, name):
        return np.array([getattr(elm, name) for elm in self._list_of_point])

    @property
    def delta_phi(self):
        return unwrap_phase(self.get_column('delta_phi'))

    @property
    def gain(self):
        return self.get_column('gain')

    @property
    def freq(self):
        return self.get_column('freq')

    def plot_matplotlib(self, fig=None):
        if fig is None:
            from matplotlib.pyplot import figure
            fig = figure()
        from matplotlib.ticker import NullFormatter, MultipleLocator
        # see http://wittman.physics.ucdavis.edu/Matplotlib-examples/
        axe1 = fig.add_subplot(2,1,1)
        axe1.plot(self.freq, 20*np.log(self.gain)/np.log(10), 'o-')
        axe1.set_xscale('log')
        axe1.yaxis.set_major_locator(MultipleLocator(10))
        for tick in axe1.get_xticklabels():
            tick.set_visible(False)
        axe1.grid(True)
        axe1.set_ylabel('Gain (dB)')
        axe2 = fig.add_subplot(2,1,2, sharex=axe1)
        axe2.plot(self.freq, self.delta_phi*180/np.pi, 'o-')
        axe2.set_xscale('log')
        fig.subplots_adjust(hspace=.01)
        axe2.set_xlabel('Frequence (Hz)')
        axe2.set_ylabel('Phase (deg)')
        axe2.grid(True)
        yticks = axe2.yaxis.get_major_ticks()
        yticks[-1].label1.set_visible(False)
        if self.title:
            axe1.set_title(self.title)

    plot = plot_matplotlib # default plot


class BodePoint(object):
    def __init__(self, t, y, y_ref, freq):
        self.t = t
        self.y = y
        self.y_ref = y_ref
        self.freq = freq

    @cached_property
    def fit_parameter(self):
        return self.fit()

    def fit(self):
        out = {}
        out.update(fit_sinusoid(self.t, self.y, freq=self.freq, postfix=''))
        out.update(fit_sinusoid(self.t, self.y_ref, freq=self.freq, postfix='_ref'))
        return out

    for key in ['offset', 'amplitude', 'frequency', 'phase']:
        for i in ['','_ref']:
            f = eval('lambda self:self.fit_parameter["{key}{i}"]'.format(key=key, i=i))
            locals()[key+str(i)] = property(f)

    @property
    def delta_phi(self):
        return self.phase - self.phase_ref

    @property
    def gain(self):
        return self.amplitude/self.amplitude_ref
