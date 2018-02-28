import os
import tempfile
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


from multiprocessing import Queue, Process

class PyQtPlotGraphicsTestBis(Process):
    def __init__(self, filename=None):
        self.queue = Queue(1)
        self.filename = filename
        super(PyQtPlotGraphicsTestBis, self).__init__()

    def run(self):
        app = pg.QtGui.QApplication([])
        self.view = pg.GraphicsView()

        self.plot()

        def tick():
            p = pg.Qt.QtGui.QApplication.primaryScreen().grabWindow(self.view.winId())
            if self.filename is not None:
                p.save(os.path.join(tempfile.gettempdir(), self.filename), 'jpg')
            app.exit()    

        timer = pg.Qt.QtCore.QTimer()
        timer.timeout.connect(tick)
        timer.start(100)

        app.exec_()

        self.queue.put(None)
        
    def plot(self):
        raise Exception('Please create the plot to test')

    def test(self):
        self.start()
        self.join()

