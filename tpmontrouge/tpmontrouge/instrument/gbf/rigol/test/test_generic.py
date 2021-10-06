import unittest
from ..generic import Rigol

from ...test.test_gbf import GenericTest
from ....utils.instrument import FakeSCPI


class TestTektonix(GenericTest, unittest.TestCase):
    gbf = Rigol(FakeSCPI())
