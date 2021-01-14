#from .scope import scope_factory
#from .gbf import gbf_factory

#from .connection.device_info import AllDevices
#from .connection import get_all_connected_devices
#from .connection import auto_connect

from .scope import Scope
from .gbf import GBF
from .voltmeter import Voltmeter
from .analog_input import AnalogInput

instrument_str = ['Scope', 'GBF', 'Voltmeter', 'AnalogInput']

from .connection.list_all_devices import get_all_connected_devices, get_first_device

from .connection import list_all_devices
list_all_devices._make_doc(instrument_str)
del list_all_devices

