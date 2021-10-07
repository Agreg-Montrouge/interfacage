#from __future__ import absolute_import

#try:
#    import visa 
#except ImportError:
#    visa = None


#if visa is not None:
#    rm = visa.ResourceManager()
#    open_resource = rm.open_resource
#else:
#    def open_resource(*args, **kwd):
#        raise Exception('Visa not installed on your computer') 

import pyvisa
from .device_info import DeviceInfo, AllDevices

rm = pyvisa.ResourceManager()
open_resource = rm.open_resource

class VISADeviceInfo(DeviceInfo):
    def get_connection(self):
        device_str = self._device_str
        if device_str.lower().startswith('asrl'):
            raise Exception('Unsupported')

        if device_str.lower().startswith('usb'):
            sp_str = device_str.split('::')
            if len(sp_str)>=4 and (sp_str[1]=='0x1AB1' or sp_str[1]=='0x0A00') and sp_str[3].lower().startswith('dg'):
                return rm.open_resource(self._device_str, query_delay=0.001) 
        return rm.open_resource(self._device_str)

def list_device_str():
    return rm.list_resources()

def _auto_detect():
    for elm in list_device_str():
        elm = VISADeviceInfo(elm)
        try:
            elm.idn
        except:
            continue
        yield elm

def auto_detect_visa():
    return list(_auto_detect())

AllDevices.add_autodetect_function(auto_detect_visa)

