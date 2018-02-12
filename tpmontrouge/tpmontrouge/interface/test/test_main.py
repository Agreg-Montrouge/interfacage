import os
import tempfile
import unittest
import pyqtgraph as pg

from ..main import MainWindow


class Test(unittest.TestCase):
    def test(self):
        app = pg.QtGui.QApplication([])
        win = MainWindow()

        def tick():
            p = pg.Qt.QtGui.QApplication.primaryScreen().grabWindow(win.winId())
            p.save(os.path.join(tempfile.gettempdir(), 'test_main_app.jpg'), 'jpg')
            app.exit()    

        timer = pg.Qt.QtCore.QTimer()
        timer.timeout.connect(tick)
        timer.start(200)

        win.show()
        app.exec_()

        del app


