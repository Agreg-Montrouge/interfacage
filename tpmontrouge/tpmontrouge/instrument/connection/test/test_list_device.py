import unittest
from ..device_info import AllDevices

from ..list_all_devices import get_all_connected_devices

from ...scope.test import test_detection
from ...gbf.test import test_detection
from ...scope import Scope

class Test(unittest.TestCase):
    def test(self):
        all_devices = AllDevices()

    def test_function(self):
        self.assertEqual(len(get_all_connected_devices('Scope')), 3)
        self.assertEqual(len(get_all_connected_devices(Scope)), 3)

if __name__=='__main__':
    all_devices = AllDevices()
    print(all_devices.list_of_devices)
