import argparse

from pyqtgraph.Qt import QtCore, QtGui
from .scope import get_scope_window
from .bode_plot import get_bode_window
from .. import plot_engine

class MainWindow(QtGui.QTabWidget):
    plot_engine=plot_engine
    def __init__(self, plot_engine=None):
        super().__init__()
        plot_engine = plot_engine or self.plot_engine

        self.addTab(get_scope_window(plot_engine=plot_engine),"Oscilloscope")
        self.addTab(get_bode_window(plot_engine=plot_engine),"Diagramme de Bode")

def main(argv=[]):
    parser = argparse.ArgumentParser(description='Programme principale pour le TP de Montrouge')
    parser.add_argument('--test', action='store_true', help='Use to test unconnected instrument')
    parser.add_argument('--plot_engine', default='pyqtgraph', help='Engine to do the plots', choices=['mpl', 'pyqtgraph'])

    args = parser.parse_args(argv[1:])
    if args.test:
            from ..instrument.scope.test import test_detection
            from ..instrument.gbf.test import test_detection
    app = QtGui.QApplication([])
    win = MainWindow(args.plot_engine)
    win.show()
    app.exec_()


if __name__=='__main__':
    import sys
    main(sys.argv)
