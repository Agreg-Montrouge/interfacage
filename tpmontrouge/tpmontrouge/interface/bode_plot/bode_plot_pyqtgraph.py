import pyqtgraph
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from time import sleep

from . import bode_plot_common
class BodeExperiment(bode_plot_common.BodeExperiment):
    pass
#    def display_last_point(self, last_point):
#        super(BodeExperiment, self).display_last_point(last_point)
#        self.thread.emit(QtCore.SIGNAL('new_loop(PyQt_PyObject, PyQt_PyObject)'), last_point, self._bode_plot)
        # Faire quelquechose comme envoyer un signal avec un objet. 
#        if self.scope_figure is not None:
#            view = self.scope_figure
#            last_point.plot_pyqtgraph(view)
#        if self.bode_figure is not None:
#            view = self.bode_figure 
#            self._bode_plot.plot_pyqtgraph(view, log_scale=self.log_scale)
#        print('HELLO'*100)
#        sleep(10)


class BodeWindows(bode_plot_common.BodeWindows):
    bode_experiment = BodeExperiment
    def add_plot_widgets(self):
        plot1 = pg.GraphicsView() 
        tmp_layout = QtGui.QVBoxLayout()
        tmp_layout.addWidget(plot1)
        tmp_layout.addStretch(1)
        self.main_layout.addLayout(tmp_layout)
        plot2 = pg.GraphicsView() 
        tmp_layout = QtGui.QVBoxLayout()
        tmp_layout.addWidget(plot2)
        tmp_layout.addStretch(1)
        self.main_layout.addLayout(tmp_layout)

        self.plot1 = plot1
        self.plot2 = plot2

    def end_of_one_iteration(self, data):
        last_point, bode_plot = data
        last_point.plot_pyqtgraph(self.plot1)
        bode_plot.plot_pyqtgraph(self.plot2)



class BodeThread(bode_plot_common.BodeThread):
    @property
    def exp(self):
        return BodeExperiment(self.gbf, self.scope, 
                                self.scope.channel[self.parameters['Sig. chan.']], 
                                self.scope.channel[self.parameters['Ref. chan.']], 
                                disp=True, wait_time=0,
                                scope_mpl_figure=self.bode_windows.plot1, 
                                bode_mpl_figure=self.bode_windows.plot2,
                                log_scale = self.parameters['log'])

if __name__=='__main__':
    app = pg.QtGui.QApplication([])
    win = BodeWindows()
    win.show()
    app.exec_()

