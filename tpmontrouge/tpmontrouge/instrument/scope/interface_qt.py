from ..connection import interface_qt
from . import scope_factory, get_all_scopes

from ...instrument.scope.scope import Scope
from ...experiment.test.virtual_instrument_for_bode_plot import RootScope

class ScopeConnection(interface_qt.Connection):
    name = 'Scope'
    default = 'Simulation'
    kind_of_model = Scope

    @property
    def simulated_instrument(self):
        return Scope(RootScope())


