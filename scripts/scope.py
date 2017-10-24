# -*- coding: utf-8 -*-

from tpmontrouge.instrument import scope_factory

scope = scope_factory('GPIB0::1::INSTR')

fig = figure() # Il faut avoir lanser %pylab

wfm = scope.channel1.get_waveform()
wfm.plot(fig)

