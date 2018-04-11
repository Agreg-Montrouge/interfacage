from .utils import unable_to_open
from sys import platform

if platform=="linux" or platform=="linux2":
    from ._usbtmc import *
else:
    USBTMC = None
    USBTMCDeviceInfo = unable_to_open
