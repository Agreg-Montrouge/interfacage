from .usbtmc import USBTMC
from .visa import open_resource
#from serial import Serial

def auto_connect(info):
    if 'usbtmc' in info.lower():
        return USBTMC(info)
#    if 'COM' in info:
#        return Serial(info)
    if '::' in info:
        return open_resource(info)
    raise ValueError('Unknown resource information "{}"'.format(info))

