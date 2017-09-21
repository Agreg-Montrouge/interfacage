import unittest

from ..impedance import *

class Test(unittest.TestCase):
    def test(self):
        self.assertEqual(FiftyOhm, 50)
        self.assertEqual(50, FiftyOhm)
        self.assertTrue(SeventyFiveOhm>50)
        self.assertTrue(50<SeventyFiveOhm)
        self.assertEqual('FiftyOhm', FiftyOhm)
        self.assertIs(convert('FiftyOhm'), FiftyOhm)    

    def test_dct(self):
        dct = {FiftyOhm:'FIFty'}
        val = 50
        self.assertEqual(dct[convert(val)], 'FIFty')
