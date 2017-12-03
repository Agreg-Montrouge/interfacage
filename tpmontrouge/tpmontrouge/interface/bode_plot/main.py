import pyqtgraph as pg

from .bode_plot import BodeWindows

def main(argv=[]):
    if len(argv)>1:
        if argv[1]=="test":
            from ...instrument.scope.test import test_detection
            from ...instrument.gbf.test import test_detection
    app = pg.QtGui.QApplication([])
    win = BodeWindows()
    win.show()
    app.exec_()

