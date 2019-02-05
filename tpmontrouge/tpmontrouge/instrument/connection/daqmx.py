from .utils import unable_to_open

try:
    from ._daqmx import *

except ImportError:
    def open_resource(*args, **kwd):
        raise Exception('Visa not installed on your computer') 
    PyDAQmx = None
    DAQmxDeviceInfo = unable_to_open

