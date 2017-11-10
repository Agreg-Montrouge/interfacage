import pyqtgraph as pg

from .bode_plot import BodeWindows

def main(argv=[]):
    app = pg.QtGui.QApplication([])
    win = BodeWindows()
    win.show()
    app.exec_()

