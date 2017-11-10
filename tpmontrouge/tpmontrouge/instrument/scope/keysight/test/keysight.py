import unittest
from ..generic import Keysight

from ...test.test_scope import GenericTest

class TestKeysight(GenericTest, unittest.TestCase):
#    scope = Tektronix(inst)
    
    def test_base(self):
        self.scope.autoset()
        self.assertEqual(self.scope._root._last_command.lower(), 'autoscale')


    def test_IDN(self):
        idn = self.scope.ask('*IDN?')
        self.assertIn("AGILENT", idn)
        
    def test_channel(self):
        pass

from ....connection.usbtmc import USBTMC
conn = USBTMC()
scope = Keysight(conn)
TestKeysight.scope = scope

# AGILENT TECHNOLOGIES,DSO-X 2002A,MY57235663,02.42.2017032900
if __name__=="__main__":
#    import visa
#    import sys
#    rm = visa.ResourceManager()
#    if len(sys.argv)>1:
#        resource = sys.argv.pop()
#    else:
#        resource = 'GPIB0::1::INSTR'
#    inst = rm.open_resource(resource)
#    TestTektonix.inst= inst
#    unittest.main()
    unittest.main()
