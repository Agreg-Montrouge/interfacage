from .device_info import AllDevices

if __name__=="__main__":
    all_devices = AllDevices()
    print(all_devices.list_of_devices)
    print(list(all_devices.get_all_connected_devices()))
