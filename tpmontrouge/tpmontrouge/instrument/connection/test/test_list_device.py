import unittest
from ..device_info import AllDevices

class Test(unittest.TestCase):
    def test(self):
        all_devices = AllDevices()

if __name__=='__main__':
    all_devices = AllDevices()
    print(all_devices.list_of_devices)
