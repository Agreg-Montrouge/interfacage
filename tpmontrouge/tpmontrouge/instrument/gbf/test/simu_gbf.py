from ..constant import function

class GBFSimulation(object):
    def on_command(self):
        self._last_command = "on"

    def off_command(self):
        self._last_command = "off"


    _frequency = 1
    def get_frequency(self):
        return self._frequency

    def set_frequency(self, val):
        self._frequency = val

    _amplitude = 1
    def get_amplitude(self):
        return self._amplitude

    def set_amplitude(self, val):
        self._amplitude = val

    _offset = 0
    def get_offset(self):
        return self._offset

    def set_offset(self, val):
        self._offset = val

    _function = function.Sinusoid
    def get_function(self):
        return self._function

    def set_function(self, val):
        self._function = function.convert(val)



