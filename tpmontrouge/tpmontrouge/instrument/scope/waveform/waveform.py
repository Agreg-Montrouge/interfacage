import numpy as np

class Waveform(object):
    def __init__(self, data, t0, dt):
        self.data = data
        self.t0 = t0
        self.dt = dt

    @property
    def N(self):
        return len(self.data)

    @property
    def x_data(self):
        return np.arange(self.N)*self.dt + self.t0


    @property
    def y_data(self):
        return self.data

    @property
    def x_label(self):
        return 'Temps [s]'

    @property
    def y_label(self):
        return 'Tension [V]'

    def plot_matplotlib(self, fig=None, axes=None, **kwd):
        if fig is not None:
            assert axes is None
            axes = fig.add_subplot(1,1,1)
        axes.plot(self.x_data, self.y_data, **kwd)
        axes.set_xlabel(self.x_label)
        axes.set_ylabel(self.y_label)     


    plot = plot_matplotlib
