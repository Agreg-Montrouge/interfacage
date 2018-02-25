import unittest

from ..main import MainWindow
from .utils import ProcessApp


#class MyApp(Process):
#    def __init__(self, main_windows_class, filename=None):
#        self.queue = Queue(1)
#        self.main_windows_class = main_windows_class
#        self.filename = filename
#        super(MyApp, self).__init__()

#    def run(self):
#        app = pg.QtGui.QApplication([])
#        win = self.main_windows_class()

#        def tick():
#            p = pg.Qt.QtGui.QApplication.primaryScreen().grabWindow(win.winId())
#            if self.filename is not None:
#                p.save(os.path.join(tempfile.gettempdir(), self.filename), 'jpg')
#            app.exit()    

#        timer = pg.Qt.QtCore.QTimer()
#        timer.timeout.connect(tick)
#        timer.start(200)

#        win.show()
#        app.exec_()

#        self.queue.put(None)
#        
#    
#app1 = MyApp()
#app1.start()
#app1.join()
#print("App 1 returned: " + app1.queue.get())

class Test(unittest.TestCase):
    def test(self):
        app = ProcessApp(MainWindow, filename='test_main_app.jpg')
        app.start()
        app.join()

