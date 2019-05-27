from ..voltmeter import Voltmeter
from ...utils.instrument import Instrument
from ...autodetection.manufacturer import agilent_technologies, hewlett_packard, keysight
from ...utils.scpi import is_equal

class Agilent(Voltmeter, Instrument):
    manufacturer = agilent_technologies
    def __init__(self, *args, **kwd):
        Instrument.__init__(self, *args, **kwd)
        Voltmeter.__init__(self, root=self)
        
    def get_value(self):
        return self.scpi_ask_for_float('READ?')

class HewlettPackard(Agilent):
    manufacturer = hewlett_packard

class Keysight(Agilent):
    manufacturer = keysight

#Agilent.add_class_to_manufacturer('34450A')
#Agilent.add_class_to_manufacturer('34401A')
#Agilent.add_class_to_manufacturer('34461A')

#HewlettPackard.add_class_to_manufacturer('34450A')
#HewlettPackard.add_class_to_manufacturer('34401A')

Keysight.add_class_to_manufacturer('34450|34401|34461')
Agilent.add_class_to_manufacturer('34450|34401|34461')
HewlettPackard.add_class_to_manufacturer('34450|34401')
