import os
from .device_info import AllDevices


def get_all_connected_devices(kind_of_model=None):
    from ... import instrument
    if isinstance(kind_of_model, str):
        try:
             kind_of_model=getattr(instrument, kind_of_model)
        except AttributeError:
            raise Exception('Unkown kind of model "%s"'%kind_of_model)
    return list(AllDevices().get_all_connected_devices(kind_of_model=kind_of_model))

def get_all_connected_instruments(kind_of_model=None):
    return [elm.get_interface() for elm in get_all_connected_devices(kind_of_model)]

def get_first_device(kind_of_model):
    from ... import instrument
    if isinstance(kind_of_model, str):
        try:
             kind_of_model=getattr(instrument, kind_of_model)
        except AttributeError:
            raise Exception('Unkown kind of model "%s"'%kind_of_model)
    res = AllDevices().get_first_device(kind_of_model=kind_of_model)
    if res is not None:
        return res
    if os.getenv('SIMUMONTROUGE'):
        return FakeDevice(kind_of_model.get_simulated_device())
    raise Exception('No device of class {}. Use SIMUMONTROUGE env variable to return simulated instrument'.format(kind_of_model))

def get_first_instrument(kind_of_model):
    return get_first_device(kind_of_model).get_interface()
    
class FakeDevice(object):
    def __init__(self, instrument):
        """ Create a Fake device 

intrument : simulated instrument that will be return by the fake device
"""
        self._instrument = instrument

    def get_instrument(self):
        return self._instrument

    def __repr__(self):
        return "FakeDevice({!r})".format(self._instrument)

def _make_doc(instrument_list):
    doc = """List all the connected devices

The model can be precised either as an instrument class or a string. 

Possible instrument are : {}

Example : 

    from tpmontrouge.instrument import get_all_connected_devices
    scope_list = get_all_connected_devices('Scope')
    print(scope_list)
    my_scope = scope_list[0].get_interface()
"""
    get_all_connected_devices.__doc__ = doc.format(', '.join(instrument_list))

if __name__=="__main__":
    all_devices = AllDevices()
    print(all_devices.list_of_devices)
    print(list(all_devices.get_all_connected_devices()))
