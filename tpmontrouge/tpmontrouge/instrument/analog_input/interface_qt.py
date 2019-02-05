from ..connection import interface_qt

from .test.simu_ai import AnalogInputThreadSimulation
from .analog_input import AnalogInput

class AIConnection(interface_qt.Connection):
    name = 'Analog Input'
    default = 'Simulation'
    kind_of_model = AnalogInput

    @property
    def simulated_instrument(self):
        return AnalogInputThreadSimulation('Simulation')


