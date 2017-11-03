from time import sleep

import numpy as np

from ..analyse.Bode import BodePoint, BodePlot

class BodeExperiment(object):
    _wait_time = 1.5
    def __init__(self, gbf, scope, input_channel, reference_channel, disp=True, wait_time=None):
        self.gbf = gbf
        self.scope = scope
        self.input_channel = input_channel
        self.reference_channel = reference_channel
        self._disp = disp
        if wait_time is not None:
           self._wait_time = wait_time 
        self.configure_default_gbf()
        self.init_bode_plot()

    def init_bode_plot(self):
        self._bode_plot = BodePlot()
        

    def set_gbf_property(self, **kwd):
        for key, elm in kwd.items():
            setattr(self.gbf, key, elm)

    def configure_default_gbf(self):
        self.set_gbf_property(amplitude=1, function='Sinusoid', offset=0)

    def record_point(self, freq, auto_set=False):
        self.display_txt('Frequency : {}'.format(freq))
        self.gbf.frequency = freq
        if auto_set:
            self.scope.autoset()
            if self._wait_time>0:
                sleep(self._wait_time)
        else:
            self.scope.horizontal.scale = 1/freq
            sleep(20/freq)
        self.scope.stop_acquisition()
        input_wfm = self.input_channel.get_waveform()
        ref_wfm = self.reference_channel.get_waveform()
        self.scope.start_acquisition()
        t = input_wfm.x_data
        y = input_wfm.y_data
        ref = ref_wfm.y_data
        last_point = BodePoint(t, y, ref, freq=freq)
#        self.display(last_point.delta_phi)
        self._bode_plot.append(last_point)
        self.display_last_point(last_point)

    def display_last_point(self, last_point):
        msg = '\tPhi={}, gain={}'.format(last_point.delta_phi, last_point.gain)
        self.display_txt(msg)

    def record_bode_diagramm(self, list_of_frequency=None, start=None, stop=None, step=None, auto_set=False):
        if list_of_frequency is None:
            list_of_frequency = np.logspace(np.log10(start), np.log10(stop), step, endpoint=False)
        self.init_bode_plot()
        self.display_txt('Start of measurement')
        for freq in list_of_frequency:
            self.record_point(freq, auto_set=auto_set)
        self.display_txt('End of measurement')
        return self._bode_plot

    def display_txt(self, val):
        if self._disp:
            print(val)

