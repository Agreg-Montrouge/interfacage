from .utils import unable_to_open

try:
    from ._serial import Serial, auto_detect, SerialDeviceInfo
except ImportError:
    Serial = None
    SerialDeviceInfo = unable_to_open
