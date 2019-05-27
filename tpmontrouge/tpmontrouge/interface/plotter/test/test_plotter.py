import os
import unittest
import tempfile


from tpmontrouge.instrument.connection.device_info import AllDevices
from ...test.utils import ProcessApp
from ..plotter import PlotterWindow


class TestScopeExperimentWindows(unittest.TestCase):
#    def test_mpl(self):
#        app = ProcessApp(get_scope_window, filename='test_scope_app_mpl.jpg', plot_engine='mpl')
#        app.start()
#        app.join()

    def test_pyqtgraph(self):
        app = ProcessApp(PlotterWindow, filename='test_plotter_app_pyqtgraphb.jpg', shut_down_delay = 3000)
        app.start()
        app.join()

