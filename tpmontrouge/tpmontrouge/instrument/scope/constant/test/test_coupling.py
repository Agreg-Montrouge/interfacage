import unittest

from ..coupling import *

class Test(unittest.TestCase):
    def test(self):
        self.assertEqual(AC, 'AC')
        self.assertEqual(AC, convert('AC'))


