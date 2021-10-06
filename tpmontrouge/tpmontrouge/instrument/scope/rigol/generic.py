""" This is the generic module for Tektronix scope

It seams that the commands are the same for all the instrument

Instrument specific commands should be in a specific module
"""

import numbers

import numpy as np

from ...utils.instrument import Instrument
from ...autodetection.manufacturer import rigol
from ...scope.scope import Scope
from ...utils.scpi import is_equal

from ..constant import impedance
from ..constant import coupling
from ..constant import slope
from ..waveform import Waveform

class Rigol(Scope, Instrument):
    manufacturer = rigol
    def __init__(self, *args, **kwd):
        Instrument.__init__(self, *args, **kwd)
        Scope.__init__(self, root=self)

    def autoset_command(self):
        self.write(':AUTO')

    def start_acquisition_command(self):
        self.write(':RUN')

    def stop_acquisition_command(self):
        self.write(':STOP')

#    def stop_after_acquisition_command(self, timeout):
#        self.write(':STOP')
#        first = True
#        t0 = time()
#        while time()<t0+timeout:
#            try:
#                a = int(self.ask(':WAV:POIN?'))
#                if a<1:
#                    raise Exception
#            except Exception as e:
#                if first:
#                    self.write(':DIGitize')
#                    first = False
#                sleep(0.1)
#                pass
#            else:
#                break
#        else:
#            raise TimeoutException('Scope was not triggered before timeout ({}s)'.format(timeout))

    def scpi_channel_write(self, channel, cmd, *args):
        self.scpi_write(':CHANNEL{channel}:{cmd}'.format(channel=channel, cmd=cmd), *args)

    def scpi_channel_ask(self, channel, cmd):
        return self.scpi_ask(':CHANNEL{channel}:{cmd}'.format(channel=channel, cmd=cmd))

    def scpi_channel_ask_for_float(self, channel, cmd):
        return self.scpi_ask_for_float(':CHANNEL{channel}:{cmd}'.format(channel=channel, cmd=cmd))


    def set_channel_impedance(self, val, channel=None):
        raise Exception('Cannot set impedance for this scope')        

    def get_channel_impedance(self, val, channel=None):
        return impedance.OneMegOhm

#    impedance_to_str = {impedance.OneMegOhm:'ONEMeg', impedance.Max:'ONEMeg'}
#    def set_channel_impedance(self, val, channel=None):
#        """ Set the impedance of a channel

#        Parameters:
#            val : impedance value (number or Impedance instance)
#            channel : name of the channel
#        """
#        val = impedance.convert(val)
#        impedance_str = self.impedance_to_str.get(val, None)
#        if impedance_str is None:
#            raise Exception('The impedance {} is not allowed for this scope'.format(val))
#        self.scpi_channel_write(channel, 'IMPedance', impedance_str)


#    def get_channel_impedance(self, channel=None):
#        """ Get the value of impedance  
#        
#        Output : 
#            impedance (Impedance instance)
#        """
#        out = self.scpi_channel_ask(channel, 'IMPedance')
#        for key, val in self.impedance_to_str.items():
#            if is_equal(val, out):
#                return key
#        raise ValueError('Unknown value {}'.format(out))

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

#    def set_data_source(self, channel):
#        self.write(':WAVeform:SOURce CHANnel{}'.format(channel))

#    def get_preamble(self):
#        # Format, Type, Points, Count, XIncrement, XOrigin, XReference, YIncrement, YOrigin, YReference
#        out = self.scpi_ask(':WAV:PRE')
#        return list(map(eval, out.strip().split(',')))

    def ask_array(self, cmd):
        self.write(cmd)
        out = self._inst.read_raw()
        return out[int(out[1:2])+2:]

    def get_channel_waveform(self, channel=1, raw_data=False, **kwd):
#        self.set_data_source(channel)
#        self.write(':WAV:FORMAT BYTE')
#        Format, Type, Points, Count, XIncrement, XOrigin, XReference, YIncrement, YOrigin, YReference = self.get_preamble()
#
        buff = self.ask_array(':WAV:DATA? CHAN{channel}'.format(channel=channel))
        res = np.array(np.frombuffer(buff, dtype = np.dtype('uint8')), dtype=int)
        if raw_data is True:
            return res
        data = (256-res-132)/200*8*self.get_channel_vertical_scale(channel)-self.get_channel_vertical_offset(channel)
        horiz_offset = self.horizontal.offset
        horiz_scale = self.horizontal.scale
        dt = horiz_scale/600*12
        t0 = horiz_offset - 6*horiz_scale
        return Waveform(data=data, t0=t0, dt=dt) 


    def set_channel_state(self, val, channel):
        self.scpi_channel_write(channel, 'DISPlay', 1 if val else 0)

    def get_channel_state(self, channel):
        return self.scpi_channel_ask(channel, 'DISPlay') == '1'

    def set_horizontal_scale(self, scale):
        self.scpi_write(":TIMebase:SCAle", scale)

    def get_horizontal_scale(self):
        return self.scpi_ask_for_float(":TIMebase:SCAle")


    def set_horizontal_offset(self, offset):
        self.scpi_write(":TIMebase:OFFSet", offset)

    def get_horizontal_offset(self):
#        print('HORIZ', self.scpi_ask("HORizontal:MAin:POSition"))
        return self.scpi_ask_for_float(":TIMebase:OFFSet")

    def get_horizontal_samplig_rate(self):
        return self.scpi_ask_for_float(':ACQuire:SAMPlingrate?')

    def set_trigger_source(self, source):
        if isinstance(source, numbers.Number):
            source = 'CHAN{}'.format(source)
        if source.startswith('CH') or source in ['EXT', 'LINE', 'WGEN']:
            self.scpi_write(':TRIGger:EDGE:SOUrce', source)
        else:
            raise Exception('Unkwown value {} for trigger source'.format(source))

    def get_trigger_source(self):
        out = self.scpi_ask(':TRIGger:EDGE:SOUrce').strip()
        if out.startswith('CHAN'):
            return int(out[-1:])
        return out

    def set_trigger_level(self, value):
        self.scpi_write(':TRIGger:EDGE:LEVel', value)

    def get_trigger_level(self):
        return self.scpi_ask_for_float(':TRIGger:EDGE:LEVel')

    def set_trigger_slope(self, value):
        value = slope.convert(value)
        value_as_str = {slope.PositiveEdge:'POS', slope.NegativeEdge:'NEG'}.get(value, None)
        if value_as_str is None:
            raise Exception('Slope {} is not allowed'.format(value))
        self.scpi_write(':TRIGger:EDGE:SLOPe', value_as_str)
    
    def get_trigger_slope(self):
        out = self.scpi_ask(':TRIGger:EDGE:Slope')
        return slope.PositiveEdge if is_equal(out, 'POS') else slope.NegativeEdge

    def set_trigger_mode(self, value):
        assert is_equal(value, 'AUTO') or is_equal(value, 'NORMal')
        self.scpi_write(':TRIGger:SWEep', value)
    
    def get_trigger_mode(self):
        self.scpi_ask(':TRIGger:SWEep')
        
    @property
    def number_of_channel(self):
        if self.model_number[-1]=='4' or self.model_number[-2]=='4':
            return 4
        return 2


#Rigol.add_class_to_manufacturer('MSO')
Rigol.add_class_to_manufacturer('DS1')
