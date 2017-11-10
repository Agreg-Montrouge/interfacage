import pyqtgraph as pg
from pyqtgraph import QtGui
from ...interface.utils.start_stop_pause import ExpThread, StateMachine

class Connection(StateMachine):
    name = ""
    _device = None
    def __init__(self, *args, **kwd):
        super(Connection, self).__init__(states=['Unconnected', 'Connected'], *args, **kwd)

        self.button = pg.QtGui.QPushButton("")
        self.choices = pg.QtGui.QComboBox()
        self.choices.addItems([])

        self.entering_unconnected()
        self.button.clicked.connect(self.connect_button_pressed)

        self.refresh_btn = QtGui.QPushButton("Reload")
#        self.refresh_btn.setFixedWidth(20)
#        self.refresh_btn.setFixedHeight(20)
#        self.refresh_btn.setIcon(QtGui.QIcon(pixmaps.getPixmap('default')))
        self.refresh_btn.clicked.connect(self.refresh)  
        self.refresh()


    def connect_button_pressed(self):
        if self.state=='Connected':
            self.set_state('Unconnected')
        elif self.state=='Unconnected':
            self.set_state('Connected')

    def entering_connected(self, previous_state=None):
        self.choices.setEnabled(False)
        self.button.setText('Disconnect')
        self.create_device()

    def entering_unconnected(self, previous_state=None):
        self.choices.setEnabled(True)
        self.button.setText('Connect')

    def make_layout(self):
        layout = pg.LayoutWidget()
        label = pg.QtGui.QLabel()
        label.setText(self.name)
        layout.addWidget(label, colspan=2)
        layout.addWidget(self.button, row=1, col=0)
        layout.addWidget(self.choices, row=1, col=1)
        layout.addWidget(self.refresh_btn, row=1, col=2)
        return layout

    def refresh(self):
        self.choices.clear()
        list_of_device = self.get_list_of_devices()
#        self.choices.addItem('Default')
#        self.choices.insertSeparator(10000)
        if list_of_device:
            self.choices.addItems(list_of_device)
            self.choices.insertSeparator(10000)
        self.choices.addItem('Simulation')

    def auto_connect(self):
        if self.get_state()=='Unconnected':
            self.entering_connected()
            self.set_state('Connected')        

    @property
    def device(self):
        device = self._device
        if device is None:
            raise Exception('No device connected')
        return device

