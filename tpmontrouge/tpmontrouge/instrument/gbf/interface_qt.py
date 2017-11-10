from ..connection.interface_qt import Connection
from . import gbf_factory, get_all_gbf

from ...experiment.test.virtual_instrument_for_bode_plot import RootGBF
from .gbf import GBF


class GBFConnection(Connection):
    name = 'GBF'
    default = 'Simulation'

    def get_list_of_devices(self):
        return get_all_gbf()

    def create_device(self):
        value = self.choices.currentText()
        if value=="Default":
            value = self.default
        if value=='Simulation':
            self._device = GBF(RootGBF())
        else:
            self._device = gbf_factory(value)

