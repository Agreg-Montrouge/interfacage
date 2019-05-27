import unittest

from ...connection.test.deviceinfotest import DeviceInfoIDN
from ...connection.device_info import AllDevices

# Put here the IDN of devices that should be detected ! 

list_for_test = ['Agilent Technologies,33220A,0,f.ff-b.bb-aa-p', 
                 ]

def factory_test_gbf():
    return [DeviceInfoIDN(elm) for elm in list_for_test]


#AllDevices.add_autodetect_function(factory_test_gbf)

class TestDetection(unittest.TestCase):
    def setUp(self):
        AllDevices.add_autodetect_function(factory_test_gbf)

    def test1(self):
        for dev in list_for_test:
            dev_info = DeviceInfoIDN(dev)
            self.assertNotEqual(dev_info.manufacturer, None, 'Device {} manufacturer not detected'.format(dev))
            self.assertNotEqual(dev_info.model_class, None, 'Device {} class not detected'.format(dev))


    def tearDown(self):
        AllDevices.clear_autodetect_functions_list()

