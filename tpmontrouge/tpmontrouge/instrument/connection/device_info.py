from cached_property import cached_property
from ..autodetection.manufacturer import list_of_manufacturer
from time import time

class AllDevices(object):
    list_of_autodetect_function = []

    @classmethod
    def add_autodetect_function(cls, func):
        cls.list_of_autodetect_function.append(func)

    @classmethod
    def clear_autodetect_functions_list(cls):
        cls.list_of_autodetect_function = []        

    def __init__(self):
        self._list_of_devices = []
        for factory_function in self.list_of_autodetect_function:
            t0 = time()
            new_devices = factory_function()
#            print('Detection :', factory_function.__name__, time()-t0)
            self._list_of_devices.extend(new_devices)

    @property
    def list_of_devices(self):
        return self._list_of_devices

    def _get_all_connected_devices(self, kind_of_model=None):
        for device in self.list_of_devices:
            try:
                model_class = device.model_class
            except Exception:
                continue
#            print(device)
            if kind_of_model is None: 
                yield device
            elif (model_class is not None) and isinstance(model_class, type) and issubclass(model_class, kind_of_model):
                yield device

    def get_all_connected_devices(self, kind_of_model=None):
        return list(self._get_all_connected_devices(kind_of_model=kind_of_model))

class DeviceInfo(object):
    def __init__(self, device_str):
        self._device_str = device_str

    def get_connection(self):
        raise Exception('The class {} does not allow connection'.format(type(self).__name__))

    @cached_property
    def idn(self):
        conn = self.get_connection()
        out = conn.ask('*IDN?')
        return out.strip().split(',')

    @property
    def manufacturer(self):
        manu_name = self.idn[0]
        return list_of_manufacturer.get(manu_name)

    @property
    def model_class(self): 
        manuf = self.manufacturer
        model_name = self.idn[1]
        return manuf.get_model_class(model_name)

    @property
    def instrument(self):
        return self.model_class(self.get_connection())

    def __str__(self):
        return self._device_str

    def __repr__(self):
        return '{self.__class__.__name__}("{self._device_str}", "{self.short_string}")'.format(self=self)
    
    @property
    def short_string(self):
        return self.idn[0] + ' ' + self.idn[1]


