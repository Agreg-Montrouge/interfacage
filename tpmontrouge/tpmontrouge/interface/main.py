from pyqtgraph.Qt import QtCore, QtGui
from .scope import scope
from .bode_plot import bode_plot

class MainWindow(QtGui.QTabWidget):
    def __init__(self):
        super().__init__()

#        tab1	= QtGui.QWidget()

#        vBoxlayout	= QtGui.QVBoxLayout()
#        pushButton1 = QtGui.QPushButton("Start")
#        pushButton2 = QtGui.QPushButton("Settings")
#        pushButton3 = QtGui.QPushButton("Stop")
#        vBoxlayout.addWidget(pushButton1)
#        vBoxlayout.addWidget(pushButton2)
#        vBoxlayout.addWidget(pushButton3)
#        tab1.setLayout(vBoxlayout)   

        self.addTab(scope.ScopeWindows(),"Oscilloscope")
        self.addTab(bode_plot.BodeWindows(),"Diagramme de Bode")

#        tabs	= QtGui.QTabWidget()
#        self.setLayout(tabs)

if __name__=='__main__':
    app = QtGui.QApplication([])
    win = MainWindow()
    win.show()
    app.exec_()
