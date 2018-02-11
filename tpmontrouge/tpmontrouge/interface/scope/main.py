import pyqtgraph as pg

def main(argv=[]):
    from . import get_scope_window
    if len(argv)>1:
        if argv[1]=="test":
            from ...instrument.scope.test import test_detection
            from ...instrument.gbf.test import test_detection
    app = pg.QtGui.QApplication([])
    win = get_bode_window()
    win.show()
    app.exec_()

