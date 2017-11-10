import unittest
import pyqtgraph as pg

from ..bode_plot import BodeWindows

app = pg.QtGui.QApplication([])

class Test(unittest.TestCase):
    def test(self):
        _ = BodeWindows()
