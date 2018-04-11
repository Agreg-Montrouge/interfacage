from time import time, sleep

import numpy as np
import pyqtgraph as pg

class PlotterLine(object):
    def __init__(self, name):
        self.name = name
        self._data = []
        self._times = []

    @property
    def data(self):
        return np.array(self._data)

    @property
    def times(self):
        return np.array(self._times)

    @property
    def y_label(self):
        return 'Tension (V)'

    def add_one_point(self, t, val):
        self._data.append(val)
        self._times.append(t)

    @property
    def last_point_as_str(self):
        return "{self.name}:{val:9.5g}".format(self=self, val = self._data[-1])


class PlotterExperiment(object):
    def __init__(self, list_of_interface, sample_rate=10, disp=True):
        self._list_of_interface = list_of_interface
        self._dt = 1/sample_rate
        self._plotter_lines = [PlotterLine(elm.name) for elm in self._list_of_interface]
        self.number_of_lines = len(self._plotter_lines)
        self._disp = disp

    def loop(self, iterator):
        next_t = self.initial_time = time()
        for _ in iterator:
            t0 = time()
            if t0<next_t:
                sleep(next_t-t0)
                t0 = time()
            next_t = t0 + self._dt
            self.record_new_point()

    def record_new_point(self):
        for plotter_line, interface in zip(self._plotter_lines, self._list_of_interface):
            plotter_line.add_one_point(time()-self.initial_time, interface.get_one_point())
        if self._disp:
            print(self.last_points_as_str)

    @property
    def last_points_as_str(self):    
        out = []
        for plotter_line, interface in zip(self._plotter_lines, self._list_of_interface):
            out.append(plotter_line.last_point_as_str)
        return '      '.join(out)
            

    def plot_matplotlib(self, fig=None):
        if fig is None:
            from matplotlib.pyplot import figure
            fig = figure()
        for i, plotter_line in enumerate(self._plotter_lines):
            axe = fig.add_subplot(self.number_of_lines, 1, i+1)
            axe.plot(plotter_line.times, plotter_line.data)
            axe.grid(True)
            axe.set_ylabel(plotter_line.y_label)
            axe.set_title(plotter_line.name)
        axe.set_xlabel('Temps (s)')
        fig.tight_layout()

    def plot_pyqtgraph(self, view):
        l = pg.GraphicsLayout()
        view.setCentralItem(l)
        view.show()
        for i, plotter_line in enumerate(self._plotter_lines):
            p0 = l.addPlot(i, 0, title=plotter_line.name, labels={'left':plotter_line.y_label, 'bottom':'Temps (s)'})
            p0.showGrid(x = True, y = True, alpha = 0.3)
            p0.plot(plotter_line.times, plotter_line.data)
        l.layout.setSpacing(0.)
        l.setContentsMargins(0., 0., 0., 0.)  



