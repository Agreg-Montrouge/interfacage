import sys
import os
from serial import Serial as _Serial
from .device_info import DeviceInfo, AllDevices

class Serial(_Serial):
    def __init__(self, port, **kwd):
        kwd['baudrate'] = kwd.get('baudrate', 19200)
        kwd['timeout'] = kwd.get('timeout', .1)
        kwd['xtscts'] = kwd.get('xtscts', True)
        super().__init__(port, **kwd)

    def write(self, val):
        super().write(val.encode('ascii')+b'\r')

    def ask(self, val):
        self.write(val)
        res = self.read()
        print('REULT of', val, res)
        return res

    def read(self):
        res = b''
        while True:
            ch = super().read()
            if ch==b'\r' or ch==b'':
                break
            res += ch
        return res.decode('ascii')

class SerialDeviceInfo(DeviceInfo):
    def get_connection(self):
        return Serial(self._device_str)

def list_device_str():
    out = []
    if 'linux' in sys.platform:
        out.extend([os.path.join('/dev', elm) for elm in os.listdir('/dev') if 'ttyUSB' in elm])
    return out

def _auto_detect():
    for elm in list_device_str():
        elm = SerialDeviceInfo(elm)
        try:
            elm.idn
        except:
            continue
        yield elm

def auto_detect_serial():
    return list(_auto_detect())

AllDevices.add_autodetect_function(auto_detect_serial)


if __name__=='__main__':
    print(auto_detect())
