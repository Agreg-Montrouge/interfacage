import sys
import argparse

from pyqtgraph.Qt import QtCore, QtGui
from .scope import get_scope_window
from .bode_plot import get_bode_window
from .plotter import get_plotter_window
from .info import get_info
from .analog_input import get_ai_window

from .. import plot_engine
from .utils.display_exception import activate_error_dialog

class MainWindow(QtGui.QTabWidget):
    plot_engine=plot_engine
    def __init__(self, plot_engine=None):
        super().__init__()
        plot_engine = plot_engine or self.plot_engine

        self.addTab(get_info(), 'Info')
        self.addTab(get_scope_window(plot_engine=plot_engine, parent=self),"Oscilloscope")
        self.addTab(get_bode_window(plot_engine=plot_engine, parent=self),"Diagramme de Bode")
        if plot_engine=='pyqtgraph':
            self.addTab(get_plotter_window(plot_engine=plot_engine, parent=self),"Table traçante")
            self.addTab(get_ai_window(plot_engine=plot_engine, parent=self),"Entrée analogique")

    def new_tab_state(self, state):
#        print('Current Tab', self.currentIndex())
        if state=='Stopped':
            for i in range(self.count()):
                self.setTabEnabled(i, True)
        else:
            for i in range(1, self.count()):
                if i!=self.currentIndex():
                    self.setTabEnabled(i, False)
                


    def test_action(self):
        self.setCurrentIndex(1)

def create_parser(parser=None):
    if parser is None:
        parser = argparse.ArgumentParser(description='Programme principale pour le TP de Montrouge')
    parser.add_argument('--test', action='store_true', help='Use to test unconnected instrument')
    parser.add_argument('--plot_engine', default='pyqtgraph', help='Engine to do the plots', choices=['mpl', 'pyqtgraph'])
    return parser


def main(args=None):
    if not isinstance(args, argparse.Namespace):
        parser = create_parser()
        args = parser.parse_args(args)
    
    if args.test:
            from ..instrument.scope.test import test_detection
            from ..instrument.gbf.test import test_detection
    activate_error_dialog()
    app = QtGui.QApplication([])
    win = MainWindow(args.plot_engine)
    win.show()
    app.exec_()


if __name__=='__main__':
    main()
