import unittest
from ..generic import Metrix

from ...test.test_gbf import GenericTest
from ....connection import auto_connect

class TestMetrix(GenericTest, unittest.TestCase):
    _gbf = None
    @property
    def gbf(self):
        if self._gbf:
            return self._gbf
        self._gbf = Metrix(self.inst)
        return self._gbf

    
    def test_IDN(self):
        print(self.gbf.ask('*IDN?'))

if __name__=='__main__':
    import sys
    if len(sys.argv)>1:
        resource = sys.argv.pop()
    else:
        resource = '/dev/ttyUSB0'
    inst = auto_connect(resource)
    TestMetrix.inst= inst
    print(inst)
    unittest.main()
