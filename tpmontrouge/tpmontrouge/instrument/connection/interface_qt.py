import pyqtgraph as pg
from pyqtgraph import QtGui
from ...interface.utils.start_stop_pause import ExpThread, StateMachine

from .device_info import AllDevices

all_devices = None # This is a global variable that can be changed by reload_devices

class Connection(StateMachine):
    name = ""
    _device = None
    def __init__(self, with_enable_button=False, *args, **kwd):
        super(Connection, self).__init__(states=['Unconnected', 'Connected', 'Disabled'], *args, **kwd)

        self._with_enable_button = with_enable_button

        self.button = pg.QtGui.QPushButton("")
        self.choices = pg.QtGui.QComboBox()
        self.choices.addItems([])

        self.label = pg.QtGui.QLabel(self.name)



        self.button.clicked.connect(self.connect_button_pressed)

        if self._with_enable_button:
            self.enable_button = pg.QtGui.QCheckBox()
            self.enable_button.stateChanged.connect(self.enable_button_changed)

        self.refresh_btn = QtGui.QPushButton("Reload")
#        self.refresh_btn.setFixedWidth(20)
#        self.refresh_btn.setFixedHeight(20)
#        self.refresh_btn.setIcon(QtGui.QIcon(pixmaps.getPixmap('default')))
        self.refresh_btn.clicked.connect(self.refresh)
        self.refresh(init=True)

        if self._with_enable_button:
            self.set_state('Disabled')
        else:
            self.set_state('Unconnected')

    def connect_button_pressed(self):
        if self.state=='Connected':
            self.set_state('Unconnected')
        elif self.state=='Unconnected':
            self.set_state('Connected')

    def enable_button_changed(self, value):
        if value:
            self.set_state('Unconnected')
        else:
            self.set_state('Disabled')

    @property
    def is_enable(self):
        return not (self.state=='Disabled')


    def entering_connected(self, previous_state=None):
#        print('Entering connected')
        self.button.setEnabled(True)
        self.choices.setEnabled(False)
        self.refresh_btn.setEnabled(True)
        self.label.setEnabled(True)
        self.button.setText('Disconnect')
        self.create_device()

    def entering_unconnected(self, previous_state=None):
#        print('Entering unconnected')
        self.button.setEnabled(True)
        self.choices.setEnabled(True)
        self.refresh_btn.setEnabled(True)
        self.label.setEnabled(True)
        self.button.setText('Connect')

    def entering_disabled(self, previous_state=None):
#        print('Entering Disabled')
        self.choices.setEnabled(False)
        self.button.setEnabled(False)
        self.refresh_btn.setEnabled(False)
        self.label.setEnabled(False)

    def make_layout(self):
        layout = pg.LayoutWidget()
        layout.addWidget(self.label, col=0)
        if self._with_enable_button:
#            tmp = pg.LayoutWidget()
            layout.addWidget(self.enable_button, col=2)
            layout.addWidget(pg.QtGui.QLabel('enable'), col=3)
            #layout.addWidget(tmp, col=2)
        layout.addWidget(self.button, row=1, col=0)
        layout.addWidget(self.choices, row=1, col=1)
        layout.addWidget(self.refresh_btn, row=1, col=2, colspan=2)
        return layout

    def refresh(self, init=False):
        self.choices.clear()
        self.reload_devices(init=init)
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

    def reload_devices(self, init=False):
        global all_devices
        if init is True : 
            if all_devices is None:
                all_devices = AllDevices()
        else:
            all_devices = AllDevices()

    def get_list_of_devices(self):
        all_devices_given_model = all_devices.get_all_connected_devices(kind_of_model=self.kind_of_model)
        dct = {}
        lst = []
        for i, dev in enumerate(all_devices_given_model):
            id_ = '{i}: {dev.short_string}'.format(i=i, dev=dev)
            lst.append(id_)
            dct[id_] = dev
        self.dct = dct
        return lst

    def create_device(self):
        value = self.choices.currentText()
        if value=="Default":
            value = self.default
        if value=='Simulation':
            self._device = self.simulated_instrument
        else:
            self._device = self.dct[value].instrument
