import os
import tempfile
import pyqtgraph as pg

from multiprocessing import Queue, Process

class ProcessApp(Process):
    shut_down_delay = 200
    def __init__(self, main_windows_class, filename=None, shut_down_delay=None, **kwd):
        self.queue = Queue(1)
        self.main_windows_class = main_windows_class
        self.filename = filename
        self.shut_down_delay = shut_down_delay if shut_down_delay is not None else self.shut_down_delay
        self.kwd = kwd
        super(ProcessApp, self).__init__()

    def run(self):
        app = pg.QtGui.QApplication([])
        win = self.main_windows_class(**self.kwd)

        def tick():
            p = pg.Qt.QtGui.QApplication.primaryScreen().grabWindow(win.winId())
            if self.filename is not None:
                p.save(os.path.join(tempfile.gettempdir(), self.filename), 'jpg')
            app.exit()

        timer = pg.Qt.QtCore.QTimer()
        timer.timeout.connect(tick)
        timer.start(self.shut_down_delay)

        if hasattr(win, 'test_action'):
            timer2 = pg.Qt.QtCore.QTimer()
            timer2.singleShot(100, win.test_action)
#            timer2.start(100)

        win.show()
        app.exec_()

        self.queue.put(None)
        

