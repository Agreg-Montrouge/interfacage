import argparse

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui


from . import get_bode_window

def create_parser(parser=None):
    if parser is None:
        parser = argparse.ArgumentParser(description='Programme pour faire un diagramme de bode')
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
    app = QtGui.QApplication([])
    win = get_bode_window(args.plot_engine)
    win.show()
    app.exec_()


if __name__=='__main__':
    main()
