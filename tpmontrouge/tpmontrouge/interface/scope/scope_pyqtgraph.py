from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg


from . import scope_common

class ScopeWindows(scope_common.ScopeWindows):
    def add_plot_widgets(self):
        plot1 = pg.GraphicsView() 
        tmp_layout = QtGui.QVBoxLayout()
        tmp_layout.addWidget(plot1)
        tmp_layout.addStretch(1)
        self.main_layout.addLayout(tmp_layout)
        self.plot1 = plot1

    def end_of_one_iteration(self, data):
        if data is None:
            return
        view = self.plot1            
        l = pg.GraphicsLayout()
        view.setCentralItem(l)
        view.show()
        for i, key in enumerate(sorted(data)):
            wfm = data[key]
            p0 = l.addPlot(i, 0, title='Channel {}'.format(key), labels={'left':'Tenstion (V)', 'bottom':'Temps (s)'})
            p0.showGrid(x = True, y = True, alpha = 0.3)
            p0.plot(wfm.x_data, wfm.y_data)


if __name__=='__main__':
    import pyqtgraph as pg
    app = pg.QtGui.QApplication([])
    win = ScopeWindows()
    win.show()
    app.exec_()

