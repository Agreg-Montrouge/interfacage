import unittest

from ..info import info

class TestInfo(unittest.TestCase):
    def test1(self):
        self.assertIn('33220', info)
        self.assertIn('Cladé', info)
