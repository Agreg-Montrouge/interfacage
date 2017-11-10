from ..connection.interface_qt import Connection
from . import scope_factory,get_all_scopes

from ...instrument.scope.scope import Scope
from ...experiment.test.virtual_instrument_for_bode_plot import RootScope

class ScopeConnection(Connection):
    name = 'Scope'
    default = 'Simulation'

    def get_list_of_devices(self):
        return get_all_scopes()

    def create_device(self):
        value = self.choices.currentText()
        if value=="Default":
            value = self.default
        if value=='Simulation':
            self._device = Scope(RootScope())
        else:
            self._device = scope_factory(value)


