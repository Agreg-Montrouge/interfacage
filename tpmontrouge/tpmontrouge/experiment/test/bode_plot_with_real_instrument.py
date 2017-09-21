import unittest
import tempfile
import os
from time import sleep

import numpy as np
from scipy import signal
import matplotlib
matplotlib.use('Agg')
from matplotlib.pyplot import figure

from ..bode_plot import BodeExperiment as BE
from ..bode_plot import BodePoint

from ...instrument.scope.tektronix.generic import Tektronix
from ...instrument.gbf.agilent.generic import Agilent

import visa

rm = visa.ResourceManager()
inst_gbf = rm.open_resource('GPIB0::10::INSTR')
inst_scope = rm.open_resource('GPIB0::1::INSTR')

class BodeExperiment(BE):
    def record_point(self, freq):
        self.display('Frequency : {}'.format(freq))
        self.gbf.frequency = freq
#        self.scope.horizontal.scale = 1/freq
        self.scope.autoset()
        sleep(1.5)
        self.scope.stop_acquisition()
        input_wfm = self.input_channel.get_waveform()
        ref_wfm = self.reference_channel.get_waveform()
        self.scope.start_acquisition()
        t = input_wfm.x_data
        y = input_wfm.y_data
        ref = ref_wfm.y_data
        return BodePoint(t, y, ref, freq=freq)

class Test(unittest.TestCase):
    def test(self):
        gbf =  Agilent(inst_gbf)
        scope = Tektronix(inst_scope)

        bode_experiment = BodeExperiment(gbf, scope, scope.channel2, scope.channel1, disp=True)

        bode_plot = bode_experiment.record_bode_diagramm(start=10000, stop=10000000, step=30)
        fig = figure()
        bode_plot.plot(fig=fig)
        fig.savefig(os.path.join(tempfile.gettempdir(), 'bode_test_with_real_instrument.pdf'))

        

