import numpy as np
from cached_property import cached_property


from .utils.fit import fit_sinusoid
from .utils import unwrap_phase

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

    def plot_matplotlib(self, fig=None, log_scale=True):
        if fig is None:
            from matplotlib.pyplot import figure
            fig = figure()
        from matplotlib.ticker import NullFormatter, MultipleLocator
        # see http://wittman.physics.ucdavis.edu/Matplotlib-examples/
        axe1 = fig.add_subplot(2,1,1)
        axe1.plot(self.freq, 20*np.log(self.gain)/np.log(10), 'o-')
        if log_scale:
            axe1.set_xscale('log')
        axe1.yaxis.set_major_locator(MultipleLocator(10))
        for tick in axe1.get_xticklabels():
            tick.set_visible(False)
        axe1.grid(True)
        axe1.set_ylabel('Gain (dB)')
        axe2 = fig.add_subplot(2,1,2, sharex=axe1)
        axe2.plot(self.freq, self.delta_phi*180/np.pi, 'o-')
        if log_scale:
            axe1.set_xscale('log')
        fig.subplots_adjust(hspace=.05)
        axe2.set_xlabel('Fréquence (Hz)')
        axe2.set_ylabel('Phase (deg)')
        axe2.grid(True)
        yticks = axe2.yaxis.get_major_ticks()
#        yticks[-1].label1.set_visible(False)
        axe2.yaxis.set_major_locator(MultipleLocator(45))
        if self.title:
            axe1.set_title(self.title)
        fig.tight_layout()

    c1, c2 = None,None
    def plot_pyqtgraph(self, view=None, log_scale=True):
#        if pw is None:
        import pyqtgraph as pg
        if self.c1 is None:
#            pw = pg.plot()
            l = pg.GraphicsLayout()
            view.setCentralItem(l)
            view.show()
            p0 = l.addPlot(0, 0, labels={'left':'Gain (dB)', 'bottom':'Fréquence (Hz)'})
            p0.showGrid(x = True, y = True, alpha = 0.3)
            p1 = l.addPlot(1, 0, labels={'left':'Phase (deg)', 'bottom':'Fréquence (Hz)'})
            ax = p1.getAxis('left')
            ax.setTickSpacing(90, 45)
            p1.showGrid(x = True, y = True, alpha = 0.3) 
            self.c1 = p0.plot(symbol='o')
            self.c2 = p1.plot(symbol='o')
        #        p1.setXLink(p0)
#            l.layout.setSpacing(0.)
#            l.setContentsMargins(0., 0., 0., 0.)
            if log_scale:
                p1.setLogMode(x=True)
                p0.setLogMode(x=True)
#        if self.title:
#            p0.setLabel('top', self.title)
        self.c1.setData(self.freq, 20*np.log10(self.gain))
        self.c2.setData(self.freq, self.delta_phi*180/np.pi)

    plot = plot_matplotlib # default plot

    def save(self, fname):
        tout = np.array([self.freq, self.gain, self.delta_phi]).T
        header = '{:24s} {:25s} {:25s}'.format('Frequency', 'gain', 'delta_phi')
        np.savetxt(fname, tout, header=header, newline='\r\n')

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

    def plot_matplotlib(self, fig=None):
        if fig is None:
            from matplotlib.pyplot import figure
            fig = figure()
        from matplotlib.ticker import NullFormatter, MultipleLocator
        axe1 = fig.add_subplot(2,1,1)
        axe1.plot(self.t, self.y)
        axe2 = fig.add_subplot(2,1,2, sharex=axe1)
        axe2.plot(self.t, self.y_ref)
        axe1.set_xlabel('T (s)')
        axe1.set_ylabel('Signal (V)')
        axe2.set_ylabel('Référence (V)')
        axe1.grid(True)
        axe2.grid(True)
        fig.tight_layout()

    plot = plot_matplotlib # default plot

    def plot_pyqtgraph(self, view):
        import pyqtgraph as pg
        l = pg.GraphicsLayout()
        view.setCentralItem(l)
        view.show()
        p0 = l.addPlot(0, 0, labels={'left':'Signal (V)', 'bottom':'Temps (s)'})
        p0.showGrid(x = True, y = True, alpha = 0.3)
        p1 = l.addPlot(1, 0, labels={'left':'Référence (V)', 'bottom':'Temps (s)'})
        p1.showGrid(x = True, y = True, alpha = 0.3) 
        p0.plot(self.t, self.y)
        p1.plot(self.t, self.y_ref)
        l.layout.setSpacing(0.)
        l.setContentsMargins(0., 0., 0., 0.)        

