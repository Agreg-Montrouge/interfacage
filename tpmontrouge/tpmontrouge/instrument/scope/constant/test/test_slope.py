import unittest

from ..slope import *

class Test(unittest.TestCase):
    def test(self):
        self.assertEqual(PositiveEdge, 'PositiveEdge')
        self.assertEqual(PositiveEdge, convert('PositiveEdge'))
        self.assertEqual(repr(PositiveEdge), 'Slope("PositiveEdge")')
        self.assertEqual(str(PositiveEdge), 'PositiveEdge')


