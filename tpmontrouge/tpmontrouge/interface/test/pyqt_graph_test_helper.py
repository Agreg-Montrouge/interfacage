from pyqtgraph.Qt import QtGui, QtCore                                              
import pyqtgraph as pg 

class PyQtPlotGraphicsTest(object):
    def __init__(self):
        self.app = QtGui.QApplication([])  
        self.view = pg.GraphicsView() 

    def exec_and_save(self, filename):
        def tick():
#            print(self.view.items())
#            self.view.scene().clear()
            p = pg.Qt.QtGui.QApplication.primaryScreen().grabWindow(self.view.winId())
#            filename = os.path.join(tempfile.gettempdir(), 'bode_test.jpg')
            p.save(filename, 'jpg')
            self.app.exit()    

        timer = pg.Qt.QtCore.QTimer()
        timer.timeout.connect(tick)
        timer.start(100)


        self.app.exec_()
        del self.app


