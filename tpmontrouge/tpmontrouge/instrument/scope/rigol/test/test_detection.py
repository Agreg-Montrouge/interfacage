import unittest
from ..generic import Rigol

from ....connection.test.deviceinfotest import DeviceInfoIDN
from ....connection.device_info import AllDevices

#list_for_test = [DeviceInfoIDN('TEKTRONIX,TDS2000,234234,V.34.123')]

#def factory():
#    return list_for_test

#class TestDetection(unittest.TestCase):
#    def setUp(self):
#        AllDevices.add_autodetect_function(factory)

#    def test1(self):
#        AllDevices.add_autodetect_function(factory)
#        dev = DeviceInfoIDN('TEKTRONIX,TDS2000,234234,V.34.123')
#        self.assertEqual(dev.manufacturer, Tektronix.manufacturer)
#        self.assertEqual(dev.model_class, Tektronix)
#    def test2(self):
#        all_devices = AllDevices()
#        self.assertIn(list_for_test[0], all_devices.get_all_connected_devices())

#    def tearDown(self):
#        AllDevices.clear_autodetect_functions_list()

