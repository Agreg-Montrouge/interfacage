import os
from .device_info import DeviceInfo, AllDevices

class USBTMC(object):
    """Simple implementation of a USBTMC device driver, in the style of visa.h
    """

    def __init__(self, device="/dev/usbtmc0"):
        self.device = device
        self.FILE = os.open(device, os.O_RDWR)

    def write(self, command):
        os.write(self.FILE, command.encode('ascii'))

    def read(self, length=None):
        if length is None:
            length = 4000
        return os.read(self.FILE, length)

    def ask(self, command, length=None):
        self.write(command)
        return self.read(length=length).decode('ascii')

    def ask_for_value(self, command):
        return eval(self.ask(command).strip())

    def getName(self):
        return self.ask("*IDN?")

    def sendReset(self):
        self.write("*RST")

class USBTMCDeviceInfo(DeviceInfo):
    def get_connection(self):
        return USBTMC(self._device_str)

def list_device_str():
    tout = os.listdir('/dev')
    return ['/dev/'+elm for elm in tout if elm.startswith('usbtmc')]

def auto_detect_usbtmc():
    return [USBTMCDeviceInfo(elm) for elm in list_device_str()]

AllDevices.add_autodetect_function(auto_usbtmc_detect)

if __name__ == "__main__":
    inst = USBTMC()
