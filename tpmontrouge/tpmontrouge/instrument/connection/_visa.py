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

def auto_detect():
    return list(_auto_detect())

AllDevices.add_autodetect_function(auto_detect)
