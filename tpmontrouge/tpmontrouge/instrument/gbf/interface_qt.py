from ..connection import interface_qt

from ...experiment.test.virtual_instrument_for_bode_plot import RootGBF
from .gbf import GBF


class GBFConnection(interface_qt.Connection):
    name = 'GBF'
    default = 'Simulation'
    kind_of_model = GBF

    @property
    def simulated_instrument(self):
        return GBF(RootGBF())


