import unittest
from ..manufacturer import list_of_manufacturer, Manufacturer
from ...scope import Scope

class TestManu(unittest.TestCase):
    def test1(self):
        manufa = list_of_manufacturer.get('TEKTRONIX')
        self.assertIsNot(manufa, None)
        
    def test2(self):
        test = Manufacturer('Test')
        test.add_model('TEST \d+', 'A')
        self.assertEqual(test.get_model_class('Test 3435'), 'A')

    def test3(self):
        all_models = list_of_manufacturer.get_all_models()
        self.assertIn('MSO', all_models['Tektronix'])
        self.assertIn('33220', all_models['Agilent Technologies'])
        all_scopes = list_of_manufacturer.get_all_models(Scope)
        self.assertIn('MSO', all_scopes['Tektronix'])
        self.assertNotIn('33220', all_scopes['Agilent Technologies'])

