import os
import unittest
import tempfile

from ..scope_common import ScopeExperiment as _ScopeExperiment
from ...test.utils import ProcessApp

from .. import get_scope_window
from ....experiment.test.virtual_instrument_for_bode_plot import RootScope
from ....instrument.scope.scope import Scope


class ScopeExperiment(_ScopeExperiment):
    def plot(self):
        pass
        

class TestScopeExperiment(unittest.TestCase):
    def testA(self):
        scope = Scope(RootScope())
        exp = ScopeExperiment(scope)

        exp.loop([1,2], delay=0)
    
        filename = os.path.join(tempfile.gettempdir(), 'test_scope.txt')
        exp.save(filename)
    def testB(self):
        scope = Scope(RootScope())
        exp = ScopeExperiment(scope)

        exp.loop([1,2], delay=None)
    
        filename = os.path.join(tempfile.gettempdir(), 'test_scope.txt')
        exp.save(filename)


#        print(filename)

class TestScopeExperimentWindows(unittest.TestCase):
    def test_mpl(self):
        app = ProcessApp(get_scope_window, filename='test_scope_app_mpl.jpg', plot_engine='mpl')
        app.start()
        app.join()

    def test_pyqtgraph(self):
        app = ProcessApp(get_scope_window, filename='test_scope_app_pyqtgraph.jpg', plot_engine='pyqtgraph')
        app.start()
        app.join()

