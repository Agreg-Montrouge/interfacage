from .device_info import AllDevices

def get_all_connected_devices(kind_of_model=None):
    from ... import instrument
    if isinstance(kind_of_model, str):
        try:
             kind_of_model=getattr(instrument, kind_of_model)
        except AttributeError:
            raise Exception('Unkown kind of model "%s"'%kind_of_model)
    return list(AllDevices().get_all_connected_devices(kind_of_model=kind_of_model)) 

def _make_doc(instrument_list):
    doc = """List all the connected devices

The model can be precised either as an instrument class or a string. 

Possible instrument are : {}

Example : 

    from tpmontrouge.instrument mport get_all_connected_devices
    scope_list = get_all_connected_devices('Scope')
    print(scope_list)
    my_scope = scope_list[0]
"""
    get_all_connected_devices.__doc__ = doc.format(', '.join(instrument_list))

if __name__=="__main__":
    all_devices = AllDevices()
    print(all_devices.list_of_devices)
    print(list(all_devices.get_all_connected_devices()))
