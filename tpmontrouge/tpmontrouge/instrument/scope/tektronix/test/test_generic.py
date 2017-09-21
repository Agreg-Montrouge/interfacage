import unittest
from ..generic import Tektronix

from ...test.test_scope import GenericTest
from ....utils.instrument import FakeSCPI

import numpy as np


dt = 1E-4
N = 1000
array_for_test = np.sin(np.arange(N)*dt*2*np.pi*50)
yscale = .5
ymult = .5 / 2**8
yoff = 5*2**8
int_array_for_test = np.array(yoff + array_for_test/ymult, dtype=np.dtype('int16').newbyteorder('>'))
buf = int_array_for_test.data.tobytes()
print(int_array_for_test[:10])
buf = b'#' + str(len(str(len(buf)))).encode() + str(len(buf)).encode() + buf

class FakeSCPITektronix(FakeSCPI):
    _record = {'CURVE':buf,
        'WFMPre:XIN':str(dt),
        'WFMPre:XZERO':'0',
        'WFMPre:YMUlt':str(ymult),
        'WFMPre:YOFf':str(yoff)}

class TestTektonix(GenericTest, unittest.TestCase):
    scope = Tektronix(FakeSCPITektronix())

    def test_base(self):
        pass
