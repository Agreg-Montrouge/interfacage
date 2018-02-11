import os
import unittest
import tempfile

from ..scope import ScopeExperiment
from ....experiment.test.virtual_instrument_for_bode_plot import RootScope
from ....instrument.scope.scope import Scope


class TestScopeExperiment(unittest.TestCase):
    def test(self):
        scope = Scope(RootScope())
        exp = ScopeExperiment(scope)

        exp.loop([1,2], delay=0)
    
        filename = os.path.join(tempfile.gettempdir(), 'test_scope.txt')
        exp.save(filename)
        print(filename)


