import sys
import os

from .visa import visa


def get_all_connection():
    out = []
    if visa is not None:
        from .visa import rm
        out.extend(rm.list_resources())
    if 'linux' in sys.platform:
        out.extend([os.path.join('dev', elm) for elm in os.listdir('/dev') if 'ttyUSB' in elm])
    return out
