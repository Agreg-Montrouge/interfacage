import unittest

from ...test.utils import ProcessApp

from .. import get_bode_window


class Test(unittest.TestCase):
    def test_mpl(self):
        app = ProcessApp(get_bode_window, filename='test_bode_app_mpl.jpg', plot_engine='mpl', shut_down_delay=2000)
        app.start()
        app.join()

    def test_pyqtgraph(self):
        app = ProcessApp(get_bode_window, filename='test_bode_app_pyqtgraph.jpg', plot_engine='pyqtgraph', shut_down_delay=2000)
        app.start()
        app.join()



if __name__=='__main__':
    app = pg.QtGui.QApplication([])
    win = BodeWindows()
    win.show()
    app.exec_()

