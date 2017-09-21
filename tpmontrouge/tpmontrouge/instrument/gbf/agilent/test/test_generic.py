import unittest
from ..generic import Agilent

from ...test.test_gbf import GenericTest
from ....utils.instrument import FakeSCPI


class TestTektonix(GenericTest, unittest.TestCase):
    gbf = Agilent(FakeSCPI())
