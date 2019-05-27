import unittest

from tpmontrouge.instrument.utils.instrument import Instrument
from ...connection.test.deviceinfotest import DeviceInfoIDN
from ...connection.device_info import AllDevices

# Put here the IDN of devices that should be detected ! 

list_for_test = ['TEKTRONIX,TDS2000,234234,V.34.123', 
                 'AGILENT TECHNOLOGIES,DSO-X 2002A,MY57235663,02.42.2017032900', 
                'TEKTRONIX,MSO3014,234234,V.34.123', 'TEKTRONIX,NOTEXISTING2000,234234,V.34.123',
                'Keysight Technologies,34461A,MY57221839,1.02.17-02.10-02.17']

def factory_scope_test():
    return [DeviceInfoIDN(elm) for elm in list_for_test]


class TestDetection(unittest.TestCase):
    def setUp(self):
        AllDevices.add_autodetect_function(factory_scope_test)

    def test1(self):
        for dev in list_for_test:
            dev_info = DeviceInfoIDN(dev)
            self.assertNotEqual(dev_info.manufacturer, None, 'Device {} manufacturer not detected'.format(dev))
            if 'NOTEXISTING' not in dev:
                self.assertTrue(issubclass(dev_info.model_class, Instrument), 'Device {} : model not detected'.format(dev))

    def tearDown(self):
        AllDevices.clear_autodetect_functions_list()

