import numpy as np

from ..analyse.Bode import BodePoint, BodePlot

class BodeExperiment(object):
    def __init__(self, gbf, scope, input_channel, reference_channel, disp=True):
        self.gbf = gbf
        self.scope = scope
        self.input_channel = input_channel
        self.reference_channel = reference_channel
        self._disp = disp
        self.configure_default_gbf()
        

    def set_gbf_property(self, **kwd):
        for key, elm in kwd.items():
            setattr(self.gbf, key, elm)

    def configure_default_gbf(self):
        self.set_gbf_property(amplitude=1, function='Sinusoid', offset=0)

    def record_point(self, freq):
        self.display('Frequency : {}'.format(freq))
        self.gbf.frequency = freq
        self.scope.autoset()
        self.scope.stop_acquisition()
        input_wfm = self.input_channel.get_waveform()
        ref_wfm = self.reference_channel.get_waveform()
        self.scope.start_acquisition()
        t = input_wfm.x_data
        y = input_wfm.y_data
        ref = ref_wfm.y_data
        return BodePoint(t, y, ref, freq=freq)

    def record_bode_diagramm(self, list_of_frequency=None, start=None, stop=None, step=None):
        if list_of_frequency is None:
            list_of_frequency = np.logspace(np.log10(start), np.log10(stop), step, endpoint=False)
        out = BodePlot()
        self.display('Start of measurement')
        for freq in list_of_frequency:
            out.append(self.record_point(freq))
        self.display('End of measurement')
        return out

    def display(self, val):
        if self._disp:
            print(val)

