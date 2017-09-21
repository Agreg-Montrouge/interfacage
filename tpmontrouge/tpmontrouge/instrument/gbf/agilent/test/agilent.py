import unittest
from ..generic import Agilent

from ...test.test_gbf import GenericTest

import visa

rm = visa.ResourceManager()
inst = rm.open_resource('GPIB0::10::INSTR')

class TestAgilent(GenericTest, unittest.TestCase):
    gbf = Agilent(inst)
    
    def test_IDN(self):
        print(inst.ask('*IDN?'))
