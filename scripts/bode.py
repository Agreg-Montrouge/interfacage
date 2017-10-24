# -*- coding: utf-8 -*-

try:
    plot
except NameError:
    raise('Il faut utiliser le mode pylab (%pylab)')
        

from tpmontrouge.instrument import scope_factory, gbf_factory
from tpmontrouge.experiment import BodeExperiment as BodeExperiment


scope = scope_factory('GPIB0::1::INSTR')
gbf = gbf_factory('GPIB0::10::INSTR')

for chan in [scope.channel1, scope.channel2]:
    chan.offset = 0
    chan.scale = .5
    

bode_experiment = BodeExperiment(gbf, scope, input_channel=scope.channel[2], 
                                 reference_channel=scope.channel[1], disp=True)
bode_plot = bode_experiment.record_bode_diagramm(start=1000, stop=1000000, 
                                                 step=30, auto_set=True)


fig = figure()
bode_plot.plot(fig)



