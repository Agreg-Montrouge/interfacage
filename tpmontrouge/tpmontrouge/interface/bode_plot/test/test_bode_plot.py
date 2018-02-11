import os
import tempfile
import unittest
import pyqtgraph as pg

from .. import get_bode_window


class Test(unittest.TestCase):
    def the_test(self, plot_engine):
        app = pg.QtGui.QApplication([])
        win = get_bode_window(plot_engine=plot_engine)

        def tick():
            p = pg.Qt.QtGui.QApplication.primaryScreen().grabWindow(win.winId())
            p.save(os.path.join(tempfile.gettempdir(), 'test_bode_app_{}.jpg'.format(plot_engine)), 'jpg')
            app.exit()    

        timer = pg.Qt.QtCore.QTimer()
        timer.timeout.connect(tick)
        timer.start(200)

        win.show()
        app.exec_()

        del app
        del win

    def test_mpl(self):
        self.the_test('mpl')

    def test_pyqtgraph(self):
        self.the_test('pyqtgraph')


if __name__=='__main__':
    app = pg.QtGui.QApplication([])
    win = BodeWindows()
    win.show()
    app.exec_()

