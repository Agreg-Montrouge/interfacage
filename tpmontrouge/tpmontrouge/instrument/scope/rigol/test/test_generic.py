import unittest
from ..generic import Rigol

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
#print(int_array_for_test[:10])
buf = b'#' + str(len(str(len(buf)))).encode() + str(len(buf)).encode() + buf + b'\n'

pre = [None, None, None, None, dt, 0, 0, ymult, 0, yoff]
pre = ', '.join([str(elm) for elm in pre])

class FakeSCPIRigol(FakeSCPI):
    _record = {':WAV:DATA':buf,
        ':WAV:PRE': pre,
        '*IDN':'RIGOL TECHNOLOGIES,MSO1104Z,DS1ZA160801111,00.04.01.'}

    def read_raw(self):
        return self._record[':WAV:DATA']


class TestRigol(GenericTest, unittest.TestCase):
    scope = Rigol(FakeSCPIRigol())

    def test_base(self):
        pass

    def test_channel_imp(self):
        pass

    def test_idn(self):
        self.assertEqual(self.scope.model_number, 'MSO1104Z')
        self.assertEqual(self.scope.number_of_channel, 4)


