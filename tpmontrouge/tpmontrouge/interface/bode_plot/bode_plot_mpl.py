import pyqtgraph
from pyqtgraph.Qt import QtCore, QtGui

from . import bode_plot_common

class BodeExperiment(bode_plot_common.BodeExperiment):
    def display_last_point(self, last_point):
        super(BodeExperiment, self).display_last_point(last_point)
        if self.scope_figure is not None:
            fig = self.scope_figure.getFigure()
            fig.clf()
            last_point.plot(fig)
            fig.canvas.draw()
        if self.bode_figure is not None:
            fig = self.bode_figure.getFigure() 
            fig.clf()
            self._bode_plot.plot(fig, log_scale=self.log_scale)
            fig.canvas.draw()



class MyMPLWidget(pyqtgraph.widgets.MatplotlibWidget.MatplotlibWidget):
    def __init__(self, *args, **kwd):
        super(MyMPLWidget, self).__init__()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHeightForWidth(True)
        self.setSizePolicy(sizePolicy)

    def heightForWidth(self, width):
        return width * 0.7

class BodeWindows(bode_plot_common.BodeWindows):
    bode_experiment = BodeExperiment
    def add_plot_widgets(self):
        plot1 = MyMPLWidget()
        tmp_layout = QtGui.QVBoxLayout()
        tmp_layout.addWidget(plot1)
        tmp_layout.addStretch(1)
        self.main_layout.addLayout(tmp_layout)
        plot2 = MyMPLWidget()
        tmp_layout = QtGui.QVBoxLayout()
        tmp_layout.addWidget(plot2)
        tmp_layout.addStretch(1)
        self.main_layout.addLayout(tmp_layout)

        self.plot1 = plot1
        self.plot2 = plot2

    def end_of_one_iteration(self, data):
        pass



if __name__=='__main__':
    import pyqtgraph as pg
    app = pg.QtGui.QApplication([])
    win = BodeWindows()
    win.show()
    app.exec_()

