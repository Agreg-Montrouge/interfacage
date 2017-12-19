import unittest
from ..generic import Tektronix

from ...test.test_scope import GenericTest

class TestTektonix(GenericTest, unittest.TestCase):
#    scope = Tektronix(inst)
    
    def test_IDN(self):
        idn = inst.ask('*IDN?')
        self.assertIn("TEKTRONIX", idn)
        
if __name__=="__main__":
    import visa
    import sys
    rm = visa.ResourceManager()
    if len(sys.argv)>1:
        resource = sys.argv.pop()
    else:
        resource = 'GPIB0::1::INSTR'
    inst = rm.open_resource(resource)
    TestTektonix.inst= inst
    print(inst)
    unittest.main()
