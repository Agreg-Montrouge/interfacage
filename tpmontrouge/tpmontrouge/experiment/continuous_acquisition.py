from __future__ import division
""" This module records data from an analog input

The data are acquired by block and concatenate
"""

from time import time, sleep

import numpy as np
import pyqtgraph as pg

class AcquisitionLine(object):
    def __init__(self, name, samplerate, channel):
        self.name = name + ' ' + channel
        self._data = []
        self._samplerate = samplerate
        self.channel = channel


    @property
    def data(self):
        return np.concatenate(self._data)

    @property
    def times(self):
        return np.arange(len(self.data))/self._samplerate

    @property
    def y_label(self):
        return 'Tension (V)'

    def add_one_block(self, val):
        self._data.append(val)

    @property
    def last_point_as_str(self):
        return "{self.name}:{val:9.5g}".format(self=self, val = self._data[-1])


class AIExperiment(object):
    def __init__(self, ai_interface, channel_list, sample_rate=100000, block_size=10000, N_block=10, disp=True):
        self._interface = ai_interface
        self._sample_rate = sample_rate
        self._block_size = block_size
        self._N_block = N_block
        self._acquisition_lines = {ch_name:AcquisitionLine(ai_interface.name, sample_rate, ch_name) for ch_name in channel_list}
        self._channel_list = channel_list
        self._disp = disp

    def loop(self, iterator=None):
        if iterator is None:
            iterator = range(self._N_block)
        self._interface.start(self._channel_list, sample_rate=self._sample_rate, block_size=self._block_size, N_block=self._N_block)
        for _ in iterator:
            self.record_new_point()
        self._interface.stop()

    def record_new_point(self):
        new_point = self._interface.get_one_block()
        for ch_name, val in new_point.items():
            self._acquisition_lines[ch_name].add_one_block(val)
        if self._disp:
            print("DISP")
            

    def plot_matplotlib(self, fig=None):
        if fig is None:
            from matplotlib.pyplot import figure
            fig = figure()
        number_of_lines = len(self._acquisition_lines)
        for i, (ch_name, ai_line) in enumerate(self._acquisition_lines.items()):
            axe = fig.add_subplot(number_of_lines, 1, i+1)
            axe.plot(ai_line.times, ai_line.data)
            axe.grid(True)
            axe.set_ylabel(ai_line.y_label)
            axe.set_title(ai_line.name)
#        axe = fig.add_subplot(1, 1, 1)
#        axe.plot(self._acquisition_line.times, self._acquisition_line.data)
#        axe.grid(True)
#        axe.set_ylabel(self._acquisition_line.y_label)
#        axe.set_title(self._acquisition_line.name)        
        axe.set_xlabel('Temps (s)')
        fig.tight_layout()

    def plot_pyqtgraph(self, view):
        l = pg.GraphicsLayout()
        view.setCentralItem(l)
        view.show()
#        for i, plotter_line in enumerate(self._plotter_lines):
#            p0 = l.addPlot(i, 0, title=plotter_line.name, labels={'left':plotter_line.y_label, 'bottom':'Temps (s)'})
#            p0.showGrid(x = True, y = True, alpha = 0.3)
#            p0.plot(plotter_line.times, plotter_line.data)
        for i, (ch_name, ai_line) in enumerate(self._acquisition_lines.items()):
            p0 = l.addPlot(i, 0, title=ai_line.name, labels={'left':ai_line.y_label, 'bottom':'Temps (s)'})
            p0.showGrid(x = True, y = True, alpha = 0.3)
            p0.plot(ai_line.times, ai_line.data)
        l.layout.setSpacing(0.)
        l.setContentsMargins(0., 0., 0., 0.)  

    def save(self, fname):
        tout = []
        header = ''
        for ch_name, ai_line in self._acquisition_lines.items():
            tout.append(ai_line.data)
            header += '{:25s}'.format(ai_line.name)
        tout = np.array(tout).T
        np.savetxt(fname, tout, header=header, newline='\r\n')

