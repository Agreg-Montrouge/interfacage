import unittest
import os
import tempfile

import matplotlib
matplotlib.use('Agg')
from matplotlib.pyplot import figure
import numpy as np
from scipy import signal

import pyqtgraph as pg
#pg.setConfigOption('background', 'w')
#pg.setConfigOption('foreground', 'k')
import pyqtgraph.exporters



from ..Bode import BodePoint, BodePlot
from ...interface.test.pyqt_graph_test_helper import PyQtPlotGraphicsTest


def generate_signal(freq):
    t = np.linspace(0, 1, 10001)
    ref = np.sin(2*np.pi*freq*t)
    b,a = signal.butter(1, [0.002, 0.004], btype='pass')
    out = signal.lfilter(b,a,ref)
    b,a = signal.butter(1, [0.02, 0.04], btype='pass')
    out = signal.lfilter(b,a,out)
    return t, ref, out



class Test(unittest.TestCase):
    def fit(self, phase=.2):
        t = np.linspace(0, 1, 101)
        freq = 4
        y1 = .6*np.sin(2*np.pi*freq*t + phase)
        y2 = .3*np.sin(2*np.pi*freq*t)
        bode_p = BodePoint(t, y1, y2, freq=freq)
        self.assertAlmostEqual(bode_p.delta_phi, phase)

    def test_fit(self):
        self.fit()

    def test_bode_plot(self):
        bode_plot = BodePlot('Filtre double')
        for freq in np.logspace(0.5, 3.5, 51):
            t, ref, out = generate_signal(freq)
            bode_plot.append(BodePoint(t, out, ref, freq=freq))
#        print(bode_plot.delta_phi)
#        print(bode_plot.gain)

        fig = figure()
        bode_plot.plot(fig=fig)
        fig.savefig(os.path.join(tempfile.gettempdir(), 'bode_test.pdf'))
        fname = os.path.join(tempfile.gettempdir(), 'test.txt')
        bode_plot.save(fname)

#    def test_bode_plot_pyqtgraph(self):
#        bode_plot = BodePlot('Filtre double')
#        for freq in np.logspace(0.5, 3.5, 51):
#            t, ref, out = generate_signal(freq)
#            bode_plot.append(BodePoint(t, out, ref, freq=freq))

#                                                             
#        app = QtGui.QApplication([])  
#        view = pg.GraphicsView()                                                            
#        bode_plot.plot_pyqtgraph(view)


#        def tick():
#            p = pg.Qt.QtGui.QApplication.primaryScreen().grabWindow(view.winId())
#            filename = os.path.join(tempfile.gettempdir(), 'bode_test.jpg')
#            p.save(filename, 'jpg')
#            app.exit()    

#        timer = pg.Qt.QtCore.QTimer()
#        timer.timeout.connect(tick)
#        timer.start(100)


#        app.exec_()
#        del app

#        return view


    def test_bode_plot_pyqtgraph(self):
        bode_plot = BodePlot('Filtre double')
        for freq in np.logspace(0.5, 3.5, 51):
            t, ref, out = generate_signal(freq)
            bode_plot.append(BodePoint(t, out, ref, freq=freq))

        app_test = PyQtPlotGraphicsTest()
        bode_plot.plot_pyqtgraph(app_test.view)
        filename = os.path.join(tempfile.gettempdir(), 'bode_test.jpg')
        app_test.exec_and_save(filename)


    

if __name__=='__main__':
    import sys
    from pyqtgraph.Qt import QtGui, QtCore                                              
    import pyqtgraph as pg                                                              
#    app = QtGui.QApplication([])                                                        

#    view = Test.test_bode_plot_pyqtgraph(None)                                                                


#    view = pg.GraphicsView()                                                            


#    l = pg.GraphicsLayout()                                                             
#    view.setCentralItem(l)                                                              
#    view.show()                                                                         
##    view.resize(800,600)                                                                
#    p0 = l.addPlot(0, 0)                                                                
#    p0.showGrid(x = True, y = True, alpha = 0.3)                                        
#    #p0.hideAxis('bottom')                                                              
#    p1 = l.addPlot(1, 0)                                                                
#    p1.showGrid(x = True, y = True, alpha = 0.3) 
#    c1 = p1.plot([1,2,3])                                       
#    c2 = p0.plot([3,1,3]) 

#    p1.setXLink(p0)                                                                     

#    l.layout.setSpacing(0.)                                                             
#    l.setContentsMargins(0., 0., 0., 0.)                                                

    def tick():
        p = pg.Qt.QtGui.QApplication.primaryScreen().grabWindow(view.winId())
        filename = os.path.join(tempfile.gettempdir(), 'bode_test.jpg')
        p.save(filename, 'jpg')
        app.exit()    

    timer = pg.Qt.QtCore.QTimer()
    timer.timeout.connect(tick)
    timer.start(100)


    app.exec_()
