from ... import instrument
from .device_info import AllDevices

def get_all_connected_devices(kind_of_model=None):
    if isinstance(kind_of_model, str):
        try:
             kind_of_model=getattr(instrument, kind_of_model)
        except AttributeError:
            raise Exception('Unkown kind of model "%s"'%kind_of_model)
    return list(AllDevices().get_all_connected_devices(kind_of_model=kind_of_model)) 

if __name__=="__main__":
    all_devices = AllDevices()
    print(all_devices.list_of_devices)
    print(list(all_devices.get_all_connected_devices()))
