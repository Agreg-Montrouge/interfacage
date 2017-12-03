from ..device_info import DeviceInfo

class DeviceInfoIDN(DeviceInfo):
    @property
    def idn(self):
        out = self._device_str
        return out.strip().split(',')

