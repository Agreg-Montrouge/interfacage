import unittest
from ..device_info import AllDevices
from .deviceinfotest import DeviceInfoIDN


from ..list_all_devices import get_all_connected_devices

#from ...scope.test import test_detection
#from ...gbf.test import test_detection
from ...scope import Scope

list_for_test_scope = ['TEKTRONIX,TDS2000,234234,V.34.123', 
                 'AGILENT TECHNOLOGIES,DSO-X 2002A,MY57235663,02.42.2017032900', 
                'TEKTRONIX,MSO3014,234234,V.34.123', 'TEKTRONIX,NOTEXISTING2000,234234,V.34.123',
                'Keysight Technologies,34461A,MY57221839,1.02.17-02.10-02.17']

def factory_scope_test():
    return [DeviceInfoIDN(elm) for elm in list_for_test_scope]


list_for_test = ['Agilent Technologies,33220A,0,f.ff-b.bb-aa-p', 
                 ]
def factory_test_gbf():
    return [DeviceInfoIDN(elm) for elm in list_for_test]


class Test(unittest.TestCase):
    def setUp(self):
        AllDevices.add_autodetect_function(factory_scope_test)
        AllDevices.add_autodetect_function(factory_test_gbf)

    def test(self):
        all_devices = AllDevices()

    def test_function(self):
        self.assertIn('AGILENT', str(get_all_connected_devices('Scope')))
        self.assertIn('AGILENT', str(get_all_connected_devices(Scope)))

    def test_doc(self):
        self.assertIn('GBF', get_all_connected_devices.__doc__)

    def tearDown(self):
        AllDevices.clear_autodetect_functions_list()

if __name__=='__main__':
    all_devices = AllDevices()
    print(all_devices.list_of_devices)
