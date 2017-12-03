import unittest
from ..manufacturer import list_of_manufacturer, Manufacturer

class TestManu(unittest.TestCase):
    def test1(self):
        manufa = list_of_manufacturer.get('TEKTRONIX')
        self.assertIsNot(manufa, None)
        
    def test2(self):
        test = Manufacturer('Test')
        test.add_model('TEST \d+', 'A')
        self.assertEqual(test.get_model_class('Test 3435'), 'A')
