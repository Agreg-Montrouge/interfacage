from ..connection import interface_qt

from .test.simu_voltmeter import VoltmeterSimulation
from .voltmeter import Voltmeter

class GBFConnection(interface_qt.Connection):
    name = 'Voltmeter'
    default = 'Simulation'
    kind_of_model = Voltmeter

    @property
    def simulated_instrument(self):
        return Voltmeter(VoltmeterSimulation())


