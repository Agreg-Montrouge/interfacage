from pyqtgraph.Qt import QtCore, QtGui
from .scope import ScopeWindows
from .bode_plot import BodeWindows

class MainWindow(QtGui.QTabWidget):
    def __init__(self):
        super().__init__()

        self.addTab(ScopeWindows(),"Oscilloscope")
        self.addTab(BodeWindows(),"Diagramme de Bode")

def main(argv=[]):
    if len(argv)>1:
        if argv[1]=="test":
            from ...instrument.scope.test import test_detection
            from ...instrument.gbf.test import test_detection
    app = QtGui.QApplication([])
    win = MainWindow()
    win.show()
    app.exec_()


if __name__=='__main__':
    main()
