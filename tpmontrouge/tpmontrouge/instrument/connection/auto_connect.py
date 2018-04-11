from .usbtmc import USBTMCDeviceInfo
from .visa import VISADeviceInfo
#from serial import Serial
from .serial import SerialDeviceInfo

def auto_connect(info):
    if 'usbtmc' in info.lower():
        return USBTMCDeviceInfo(info).instrument
    if ('COM' in info or '/dev/tty' in info):
        return SerialDeviceInfo(info).instrument
    if '::' in info:
        return VISADeviceInfo(info).instrument
#        return open_resource(info)
    raise ValueError('Unknown resource information "{}"'.format(info))


    
