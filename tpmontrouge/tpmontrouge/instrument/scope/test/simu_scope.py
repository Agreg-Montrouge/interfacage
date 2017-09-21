import numbers
import numpy as np

from ..constant import impedance
from ..constant import coupling
from ..constant import slope
from ..waveform import Waveform

class ScopeSimulation(object):
    def autoset_command(self):
        ''' Trigger an autoset on the scope '''
        self._last_command = "autoset"


    def start_acquisition_command(self):
        pass

    def stop_acquisition_command(self):
        pass


    _imp = {}
    def set_channel_impedance(self, val, channel=None):
        """ Set the impedance of a channel

        Parameters:
            val : impedance value (number or Impedance instance)
            channel : name of the channel
        """
        val = impedance.convert(val)
        self._imp[channel] = val
        
    def get_channel_impedance(self, channel=None):
        """ Get the value of impedance  
        
        Output : 
            impedance (Impedance instance)
        """
        return self._imp.get(channel, impedance.FiftyOhm)

    _coup = {}
    def set_channel_coupling(self, val, channel=None):
        self._coup[channel] = val

    def get_channel_coupling(self, channel=None):
        return self._coup.get(channel, coupling.GND)


    _vert_scale = {}
    def set_channel_vertical_scale(self, val, channel=None):
        self._vert_scale[channel] = val

    def get_channel_vertical_scale(self, channel=None):
        return self._vert_scale.get(channel, 1)


    _vert_offset = {}
    def set_channel_vertical_offset(self, val, channel=None):
        self._vert_offset[channel] = val

    def get_channel_vertical_offset(self, channel=None):
        return self._vert_offset.get(channel, 0)
    
    def get_channel_waveform(self, channel=None, **kwd):
        dt = 1E-4
        N = 10000
        t0 = -dt*N/2
        data = np.sin(100*np.arange(N)*dt)
        return Waveform(data=data, t0=t0, dt=dt) 

    def get_list_of_channel(self):
        return range(1, 5)

    _channel_state = {}
    def set_channel_state(self, val, channel):
        self._channel_state[channel] = val

    def get_channel_state(self, channel):
        return self._channel_state.get(channel, False)

    def is_active(self, channel):
        return self.get_channel_state(channel)

#    def get_list_of_active_channel(self):
#        pass


    _horiz_scale = 1
    def set_horizontal_scale(self, scale):
        self._horiz_scale = scale

    def get_horizontal_scale(self):
        return self._horiz_scale

    _horiz_offset = 0
    def set_horizontal_offset(self, value):
        self._horiz_offset = value

    def get_horizontal_offset(self):
        return self._horiz_offset

    _trigger_source = 1
    def set_trigger_source(self, source):
        self._trigger_source = source

    def get_trigger_source(self):
        return self._trigger_source

    _trigger_level = 0
    def set_trigger_level(self, value):
        self._trigger_level = value

    def get_trigger_level(self):
        return self._trigger_level

    _trigger_slope = slope.PositiveEdge
    def set_trigger_slope(self, value):
        value = slope.convert(value)
        self._trigger_slope = value
    
    def get_trigger_slope(self):
        return self._trigger_slope

    def set_trigger_coupling(self, value):
        pass    
    
    def get_trigger_coupling(self):
        pass    


    def set_trigger_mode(self, value):
        """ Auto ou normal """
        pass    
    
    def get_trigger_mode(self):
        pass    



