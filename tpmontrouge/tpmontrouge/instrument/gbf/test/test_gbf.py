import unittest

from ..gbf import GBF
from .simu_gbf import GBFSimulation

#gbf = GBF(root=self.GBFSimulation())

class GenericTest(object):
    def test_frequency(self):
        self.gbf.frequency = 100
        self.assertEqual(self.gbf.frequency, 100)

    def test_function(self):
        self.gbf.function = 'Square'
        self.assertEqual(self.gbf.function, 'Square')
        with self.assertRaises(ValueError):
            self.gbf.function = 'zer'
        self.gbf.function = 'Sinusoid'


    def test_amplitude(self):
        self.gbf.amplitude = .1
        self.assertEqual(self.gbf.amplitude, .1)

    def test_offset(self):
        self.gbf.offset = .01
        self.assertEqual(self.gbf.offset, 0.01)

    def test_on_off(self):
        self.gbf.on()
        self.gbf.off()

class TestGBFSimulation(GenericTest, unittest.TestCase):
    gbf = GBF(root=GBFSimulation())
