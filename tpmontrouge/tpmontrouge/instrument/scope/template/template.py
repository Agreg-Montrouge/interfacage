import numbers
from .. import impedance

class ScopeTemplate(object):
    def autoset(self):
        ''' Trigger an autoset on the scope '''
        pass


    def start_acquisition(self):
        pass

    def stop_acquisition(self):
        pass


    imp_to_str = [(impedance.FiftyOhm,'FIFTy'),  (impedance.Max,'MEG')]

    def set_channel_impedance(self, val, channel=None):
        """ Set the impedance of a channel

        Parameters:
            val : impedance value (number or Impedance instance)
            channel : name of the channel
        """
        val = impedance.convert(val)
        val = self.imp_to_str[val]
        pass
        
    def get_channel_impedance(self, channel=None):
        """ Get the value of impedance  
        
        Output : 
            impedance (Impedance instance)
        """
        pass
        out
        # To ensure compatibility, please return an Impedance instance
        for impedance, string in self.imp_to_str:
            if scpi.utils.equal(string, out):
                return impedance
        raise Exception('Unknown value {} for impedance').format(out)

    
    def set_channel_coupling(self, val, channel=None):
        pass

    def get_channel_coupling(self, channel=None):
        pass


    def set_channel_vertical_scale(self, val, channel=None):
        pass

    def get_channel_vertical_scale(self, channel=None):
        pass


    def set_channel_vertical_offset(self, val, channel=None):
        pass

    def get_channel_vertical_offset(self, channel=None):
        pass


    def get_channel_waveform(self, channel=None, **kwd):
        pass


    def get_list_of_channel(self)
        pass

    def set_channel_state(self, val, channel):
        pass

    def get_channel_state(self, channel):
        pass

    def is_active(self, channel):
        pass

#    def get_list_of_active_channel(self):
#        pass


    def set_horizontal_scale(self, scale):
        pass

    def get_horizontal_scale(self):
        pass

    def set_horizontal_offset(self, value):
        pass

    def get_horizontal_offset(self):
        pass



    def set_trigger_channel(self, channel):
        pass

    def get_trigger_channel(self):
        pass

    def set_trigger_level(self, value):
        pass

    def get_trigger_level(self):
        pass

    def set_trigger_slope(self, value):
        pass    
    
    def get_trigger_slope(self):
        pass    

    def set_trigger_mode(self, value):
        pass    
    
    def get_trigger_mode(self):
        pass    



