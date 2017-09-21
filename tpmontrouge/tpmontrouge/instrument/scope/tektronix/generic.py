import numbers

import numpy as np

from ...utils.instrument import Instrument
from ...scope.scope import Scope
from ...utils.scpi import is_equal

from ..constant import impedance
from ..constant import coupling
from ..constant import slope
from ..waveform import Waveform


class Tektronix(Scope, Instrument):
    def __init__(self, *args, **kwd):
        Instrument.__init__(self, *args, **kwd)
        Scope.__init__(self, root=self)

    def autoset_command(self):
        self.write('AUTOSET EXECute')

    def start_acquisition_command(self):
        self.write('ACQ:STATE RUN')

    def stop_acquisition_command(self):
        self.write('ACQ:STATE STOP')

    def scpi_channel_write(self, channel, cmd, *args):
        self.scpi_write('CH{channel}:{cmd}'.format(channel=channel, cmd=cmd), *args)

    def scpi_channel_ask(self, channel, cmd):
        return self.scpi_ask('CH{channel}:{cmd}'.format(channel=channel, cmd=cmd))

    def scpi_channel_ask_for_float(self, channel, cmd):
        return self.scpi_ask_for_float('CH{channel}:{cmd}'.format(channel=channel, cmd=cmd))

    impedance_to_str = {impedance.FiftyOhm:'FIFty',impedance.FiftyOhm:'SEVENTYFive',impedance.OneMegOhm:'MEG', impedance.Max:'MEG'}
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
        self.scpi_channel_write(channel, 'OFFS', val)

    def get_channel_vertical_offset(self, channel=None):
        return self.scpi_channel_ask_for_float(channel, 'OFFS')


    def get_out_waveform_horizontal_sampling_interval(self):
        return float(self.ask('WFMPre:XIN?'))

    def get_out_waveform_horizontal_zero(self):
        return float(self.ask('WFMPre:XZERO?'))

    def get_out_waveform_vertical_scale_factor(self):
        return float(self.ask('WFMPre:YMUlt?'))

    def get_out_waveform_vertical_offset(self):
        return float(self.ask('WFMPre:YOFf?'))

    def set_data_source(self, channel):
        self.write('DAT:SOUR CH{}'.format(channel))

    def get_channel_waveform(self, channel=None, **kwd):
        self.set_data_source(channel)
        self.write("WFMPre:ENCDG RIB")
        self.write("WFMPre:BYT_NR 2")
        offset = self.get_out_waveform_vertical_offset()
        scale = self.get_out_waveform_vertical_scale_factor()
        x_0 = self.get_out_waveform_horizontal_zero()
        delta_x = self.get_out_waveform_horizontal_sampling_interval()
        buff = self.ask_raw('CURVE?')
        res = np.frombuffer(buff, dtype = np.dtype('int16').newbyteorder('>'),
                            offset=int(buff[1:2])+2)
        data = (res - offset)*scale
        return Waveform(data=data, t0=x_0, dt=delta_x) 


    def set_channel_state(self, val, channel):
        self.scpi_write('SELECT:CH{}'.format(channel), 1 if val else 0)

    def get_channel_state(self, channel):
        self.scpi_ask('SELECT:CH{}'.format(channel)) == '1'

    def is_active(self, channel):
        return self.get_channel_state(channel)



    def set_horizontal_scale(self, scale):
        self.scpi_write("HORizontal:SCAle", scale)

    def get_horizontal_scale(self):
        return self.scpi_ask_for_float("HORizontal:SCAle")


    def set_horizontal_offset(self, offset):
        self.scpi_write("HORizontal:MAin:POSition", offset)

    def get_horizontal_offset(self):
        print('HORIZ', self.scpi_ask("HORizontal:MAin:POSition"))
        return self.scpi_ask_for_float("HORizontal:MAin:POSition")



    def set_trigger_source(self, source):
        if isinstance(source, numbers.Number):
            source = 'CH{}'.format(source)
        if source.startswith('CH') or source in ['EXT', 'EXT5', 'LINE']:
            self.scpi_write('TRIGger:MAIn:EDGE:SOUrce', source)
        raise Exception('Unkwown value {} for trigger source'.format(source))

    def get_trigger_channel(self):
        out = self.scpi_ask('TRIGger:MAIn:EDGE:SOUrce')
        if out.startswith('CH'):
            return int(out[2:])
        return out

    def set_trigger_level(self, value):
        self.scpi_write('TRIGger:MAIn:LEVel', value)

    def get_trigger_level(self):
        return self.scpi_ask_for_float('TRIGger:MAIn:LEVel')

    def set_trigger_slope(self, value):
        value = slope.convert(value)
        value_as_str = {slope.PositiveEdge:'RISe', slope.NegativeEdge:'FALL'}.get(value, None)
        if value_as_str is None:
            raise Exception('Slope {} is not allowed'.format(value))
        self.scpi_write('TRIGger:MAIn:EDGE:LEVel', value_as_str)
    
    def get_trigger_slope(self):
        out = self.scpi_ask('TRIGger:MAIn:EDGE:Slope')
        return slope.PositiveEdge if is_equal(out, 'RISe') else slope.NegativeEdge

    def set_trigger_mode(self, value):
        assert is_equal(value, 'AUTO') or is_equal(value, 'NORMal')
        self.scpi_write('TRIGger:MAIn:MODe', value)
    
    def get_trigger_mode(self):
        self.scpi_ask('TRIGger:MAIn:MODe')


class WithoutImpedance(object):
    def set_channel_impedance(self, val, channel=None):
        raise Exception('Cannot set impedance for this scope')        

    def get_channel_impedance(self, val, channel=None):
        return impedance.OneMegOhm



