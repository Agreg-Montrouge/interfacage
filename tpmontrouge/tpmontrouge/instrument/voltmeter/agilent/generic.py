from ..voltmeter import Voltmeter
from ...utils.instrument import Instrument
from ...autodetection.manufacturer import agilent_technologies
from ...utils.scpi import is_equal

class Agilent(Voltmeter, Instrument):
    manufacturer = agilent_technologies
    def __init__(self, *args, **kwd):
        Instrument.__init__(self, *args, **kwd)
        Voltmeter.__init__(self, root=self)
        
    def read_value(self):
        return self.scpi_ask_for_float('MEAS')

Agilent.add_class_to_manufacturer('34450A')
Agilent.add_class_to_manufacturer('34401A')


