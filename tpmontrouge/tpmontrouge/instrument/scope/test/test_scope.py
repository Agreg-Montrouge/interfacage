import unittest
import os
import tempfile

import matplotlib
matplotlib.use('Agg')
from matplotlib.pyplot import figure

from ..scope import Scope
from .simu_scope import ScopeSimulation


class GenericTest(object):
    scope = Scope(root=ScopeSimulation())
    def test_base(self):
        self.scope.autoset()
        self.assertEqual(self.scope._root._last_command.lower(), 'autoset')

    def test_channel(self):
        self.scope.channel[1].impedance = 'FiftyOhm'
        self.assertEqual(str(self.scope.channel[1].impedance), 'FiftyOhm')
        self.assertEqual(str(self.scope.channel1.impedance), 'FiftyOhm')
        self.scope.channel[1].coupling = 'AC'
        self.assertEqual(str(self.scope.channel[1].coupling), 'AC')
        self.scope.channel[2].offset = 0.1
        self.assertEqual(self.scope.channel[2].offset, 0.1)
        self.scope.channel[2].scale = 0.1
        self.assertEqual(self.scope.channel[2].scale, 0.1)

    def test_trigger(self):
        self.scope.trigger.slope = 'positiveedge'
        self.assertEqual(self.scope.trigger.slope, 'PositiveEdge')

        self.scope.trigger.level = .1
        self.assertEqual(self.scope.trigger.level, .1)

    def test_horizontal(self):
        self.scope.horizontal.scale = 0.01
        self.assertEqual(self.scope.horizontal.scale, 0.01)


    def test_plot(self):
        # Should be moved to test_waveform
        fig = figure()
        waveform = self.scope.channel1.get_waveform()
        waveform.plot(fig=fig)
        file = os.path.join(tempfile.gettempdir(), 'scope_test.pdf')
#        print('Figure saved to ', file)
        fig.savefig(file)

class ScopeTest(GenericTest, unittest.TestCase):
    pass
