import pyqtgraph as pg
import pyqtgraph
from pyqtgraph.Qt import QtCore, QtGui

from . import scope_common

class ScopeExperiment(scope_common.ScopeExperiment):
    def plot(self):
        if self.scope_figure:
            fig = self.scope_figure.getFigure()
            fig.clf()
            for i, key in enumerate(sorted(self.mem)):
                self.mem[key].plot_matplotlib(fig=fig)
            fig.canvas.draw()



#    def display_last_point(self, last_point):
#        super(BodeExperiment, self).display_last_point(last_point)
#        if self.scope_mpl_figure is not None:
#            fig = self.scope_mpl_figure
#            fig.clf()
#            last_point.plot(fig)
#            fig.canvas.draw()
#        if self.bode_mpl_figure is not None:
#            fig = self.bode_mpl_figure 
#            fig.clf()
#            self._bode_plot.plot(fig, log_scale=self.log_scale)
#            fig.canvas.draw()


class MyMPLWidget(pyqtgraph.widgets.MatplotlibWidget.MatplotlibWidget):
    def __init__(self, *args, **kwd):
        super(MyMPLWidget, self).__init__()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHeightForWidth(True)
        self.setSizePolicy(sizePolicy)

    def heightForWidth(self, width):
        return width * 0.7

class ScopeWindows(scope_common.ScopeWindows):
    experiment = ScopeExperiment

    def add_plot_widgets(self):
        plot1 = MyMPLWidget()
        tmp_layout = QtGui.QVBoxLayout()
        tmp_layout.addWidget(plot1)
        tmp_layout.addStretch(1)
        self.main_layout.addLayout(tmp_layout)
        self.plot1 = plot1        

if __name__=='__main__':
    app = pg.QtGui.QApplication([])
    win = ScopeWindows()
    win.show()
    app.exec_()

