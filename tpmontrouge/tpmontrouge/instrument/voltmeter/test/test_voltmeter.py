import unittest

from ..voltmeter import Voltmeter
from .simu_voltmeter import VoltmeterSimulation

class GenericTest(object):
    def test_value(self):
        self.assertEqual(self.voltmeter.get_value(), 0.1)
        self.assertEqual(self.voltmeter.get_value(), 0.2)


class TestVoltmeterSimulation(GenericTest, unittest.TestCase):
    voltmeter = VoltMeter(root=VoltmeterSimulation())
