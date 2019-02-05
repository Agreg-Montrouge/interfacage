import PyDAQmx
from ctypes import create_string_buffer

from ..autodetection.manufacturer import list_of_manufacturer
from .device_info import DeviceInfo, AllDevices

#rm = pyvisa.ResourceManager()
#open_resource = rm.open_resource

def _daqmx_str_property(function):
    n = function(None, 0)
    res = create_string_buffer(n)
    function(res, n)
    return res.value.decode()


class DAQmxDeviceInfo(object):
    def __init__(self, device_str):
        self._device_str = device_str

    @property
    def idn(self):
        return self.device_str

    def get_connection(self):
        return self

    @property
    def manufacturer(self):
        return list_of_manufacturer.get('National Instrument')

    @property
    def instrument(self):
        return self.model_class(self.get_connection())

    def __str__(self):
        return self._device_str

    def __repr__(self):
        return '{self.__class__.__name__}("{self._device_str}", "{self.short_string}")'.format(self=self)
    
    @property
    def short_string(self):
        return self._device_str


    @property
    def ai_physical_chann(self):
        print(self._device_str)
        res = _daqmx_str_property(lambda a, b:PyDAQmx.DAQmxGetDevAIPhysicalChans(self._device_str, a, b))
        return [elm.strip() for elm in res.split(',')]

class AIDAQmxDeviceInfo(DAQmxDeviceInfo):
    @property
    def model_class(self): 
        manuf = self.manufacturer
        return manuf.get_model_class('analog_input')
    

def list_device_str():
    res = _daqmx_str_property(PyDAQmx.DAQmxGetSysDevNames)
    print(res, type(res))
    for elm in res.split(','):
        elm = elm.strip()
        if DAQmxDeviceInfo(elm).ai_physical_chann!=[]:
            yield AIDAQmxDeviceInfo(elm)


def auto_detect():
    return list(list_device_str())

AllDevices.add_autodetect_function(auto_detect)
