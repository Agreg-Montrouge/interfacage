""" This is the generic module for keysight/agilent scope

It seams that the commands are the same for all the instrument

Instrument specific commands should be in a specific module
"""

import numbers

import numpy as np

from ...utils.instrument import Instrument
from ...autodetection.manufacturer import keysight
from ...scope.scope import Scope
from ...utils.scpi import is_equal

from ..constant import impedance
from ..constant import coupling
from ..constant import slope
from ..waveform import Waveform


class Keysight(Scope, Instrument):
    manufacturer = keysight
    def __init__(self, *args, **kwd):
        Instrument.__init__(self, *args, **kwd)
        Scope.__init__(self, root=self)

    def autoset_command(self):
        self.write('AUToscale')

    def start_acquisition_command(self):
        self.write(':RUN')

    def stop_acquisition_command(self):
        self.write(':STOP')

    def scpi_channel_write(self, channel, cmd, *args):
        self.scpi_write('CHANell{channel}:{cmd}'.format(channel=channel, cmd=cmd), *args)

    def scpi_channel_ask(self, channel, cmd):
        return self.scpi_ask('CHANell{channel}:{cmd}'.format(channel=channel, cmd=cmd))

    def scpi_channel_ask_for_float(self, channel, cmd):
        return self.scpi_ask_for_float('CHANell{channel}:{cmd}'.format(channel=channel, cmd=cmd))

    impedance_to_str = {impedance.OneMegOhm:'ONEMeg', impedance.Max:'ONEMeg'}
    def set_channel_impedance(self, val, channel=None):
        """ Set the impedance of a channel

        Parameters:
            val : impedance value (number or Impedance instance)
            channel : name of the channel
        """
        val = impedance.convert(val)
        impedance_str = self.impedance_to_str.get(val, None)
        if impedance_str is None:
            raise Exception('The impedance {} is not allowed for this scope'.format(val))
        self.scpi_channel_write(channel, 'IMPedance', impedance_str)


    def get_channel_impedance(self, channel=None):
        """ Get the value of impedance  
        
        Output : 
            impedance (Impedance instance)
        """
        out = self.scpi_channel_ask(channel, 'IMPedance')
        for key, val in self.impedance_to_str.items():
            if is_equal(val, out):
                return key
        raise ValueError('Unknown value {}'.format(out))

    def set_channel_coupling(self, val, channel=None):
        val = coupling.convert(val)
        self.scpi_channel_write(channel, 'COUPling', val._name)

    def get_channel_coupling(self, channel=None):
        out = self.scpi_channel_ask(channel, 'COUPling')
        return coupling.convert(out)

    def set_channel_vertical_offset(self, val, channel=None):
        self.scpi_channel_write(channel, 'OFFSet', val)

    def get_channel_vertical_offset(self, channel=None):
        return self.scpi_channel_ask_for_float(channel, 'OFFSet')

    def set_channel_vertical_scale(self, val, channel=None):
        self.scpi_channel_write(channel, 'SCALe', val)

    def get_channel_vertical_scale(self, channel=None):
        return self.scpi_channel_ask_for_float(channel, 'SCALe')



#    def get_out_waveform_horizontal_sampling_interval(self):
#        return float(self.ask('WFMPre:XIN?'))

#    def get_out_waveform_horizontal_zero(self):
#        return float(self.ask('WFMPre:XZERO?'))

#    def get_out_waveform_vertical_scale_factor(self):
#        return float(self.ask('WFMPre:YMUlt?'))

#    def get_out_waveform_vertical_offset(self):
#        return float(self.ask('WFMPre:YOFf?'))

    def set_data_source(self, channel):
        self.write(':WAVeform:SOURce CHANnel{}'.format(channel))

    def get_preamble(self):
        # Format, Type, Points, Count, XIncrement, XOrigin, XReference, YIncrement, YOrigin, YReference
        out = self.ask(':WAV:PRE?')
        return list(map(eval, out.strip().split(',')))

    def ask_array(self, cmd):
        self.write(cmd)
        first = self._inst.read(1)
        header_size = eval(self._inst.read(1))
        size_str = self._inst.read(header_size)
        while size_str[0]==b'0': # remove leading 0
            size_str = size_str[1:]
        size = int(size_str)
        output = self._inst.read(size)
        self._inst.read(1) # \n
        return output

    def get_channel_waveform(self, channel=1, **kwd):
        self.set_data_source(channel)
        self.write(':WAV:FORMAT BYTE')
        Format, Type, Points, Count, XIncrement, XOrigin, XReference, YIncrement, YOrigin, YReference = self.get_preamble()

        buff = self.ask_array(':WAV:DATA?')
        res = np.array(np.frombuffer(buff, dtype = np.dtype('uint8')), dtype=int)
        data = (res - YReference)*YIncrement
        return Waveform(data=data, t0=XOrigin, dt=XIncrement) 


#    def set_channel_state(self, val, channel):
#        self.scpi_write('SELECT:CH{}'.format(channel), 1 if val else 0)

#    def get_channel_state(self, channel):
#        self.scpi_ask('SELECT:CH{}'.format(channel)) == '1'

#    def is_active(self, channel):
#        return self.get_channel_state(channel)



    def set_horizontal_scale(self, scale):
        self.scpi_write("TIMebase:SCAle", scale)

    def get_horizontal_scale(self):
        return self.scpi_ask_for_float("TIMebase:SCAle")


    def set_horizontal_offset(self, offset):
        self.scpi_write("TIMebase:POSition", offset)

    def get_horizontal_offset(self):
#        print('HORIZ', self.scpi_ask("HORizontal:MAin:POSition"))
        return self.scpi_ask_for_float("TIMebase:POSition")



    def set_trigger_source(self, source):
        if isinstance(source, numbers.Number):
            source = 'CHANnel{}'.format(source)
        if source.startswith('CH') or source in ['EXT', 'LINE', 'WGEN']:
            self.scpi_write('TRIGger:EDGE:SOUrce', source)
        raise Exception('Unkwown value {} for trigger source'.format(source))

    def get_trigger_channel(self):
        out = self.scpi_ask('TRIGger:EDGE:SOUrce')
        if out.startswith('CH'):
            return int(out[-1:])
        return out

    def set_trigger_level(self, value):
        self.scpi_write('TRIGger:EDGE:LEVel', value)

    def get_trigger_level(self):
        return self.scpi_ask_for_float('TRIGger:EDGE:LEVel')

    def set_trigger_slope(self, value):
        value = slope.convert(value)
        value_as_str = {slope.PositiveEdge:'POS', slope.NegativeEdge:'NEG'}.get(value, None)
        if value_as_str is None:
            raise Exception('Slope {} is not allowed'.format(value))
        self.scpi_write('TRIGger:EDGE:SLOPe', value_as_str)
    
    def get_trigger_slope(self):
        out = self.scpi_ask('TRIGger:EDGE:Slope')
        return slope.PositiveEdge if is_equal(out, 'POS') else slope.NegativeEdge

    def set_trigger_mode(self, value):
        assert is_equal(value, 'AUTO') or is_equal(value, 'NORMal')
        self.scpi_write('TRIGger:SWEep', value)
    
    def get_trigger_mode(self):
        self.scpi_ask('TRIGger:SWEep')


#class WithoutImpedance(object):
#    def set_channel_impedance(self, val, channel=None):
#        raise Exception('Cannot set impedance for this scope')        

#    def get_channel_impedance(self, val, channel=None):
#        return impedance.OneMegOhm

Keysight.add_class_to_manufacturer('[DM]SO-X 2')


