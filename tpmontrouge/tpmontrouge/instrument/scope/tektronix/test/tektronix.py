import unittest
from ..generic import Tektronix

from ...test.test_scope import GenericTest

import visa

rm = visa.ResourceManager()
inst = rm.open_resource('GPIB0::1::INSTR')

class TestTektonix(GenericTest, unittest.TestCase):
    scope = Tektronix(inst)
    
    def test_IDN(self):
        idn = inst.ask('*IDN?')
        self.assertIn("TEKTRONIX", idn)
        
    def test_channel(self):
        pass
