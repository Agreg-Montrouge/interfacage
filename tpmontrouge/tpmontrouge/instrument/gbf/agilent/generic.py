from ..constant import function


from ..gbf import GBF
from ...utils.instrument import Instrument
from ...utils.scpi import is_equal

from ..constant import function

class Agilent(GBF, Instrument):
    def __init__(self, *args, **kwd):
        Instrument.__init__(self, *args, **kwd)
        GBF.__init__(self, root=self)
        
    def on_command(self):
        pass

    def off_command(self):
        pass

    def get_frequency(self):
        return self.scpi_ask_for_float('FREQ')

    def set_frequency(self, val):
        self.scpi_write('FREQ', val)

    def get_amplitude(self):
        return self.scpi_ask_for_float('VOLT')

    def set_amplitude(self, val):
        self.scpi_write('VOLT', val)

    def get_offset(self):
        return self.scpi_ask_for_float('VOLT:OFFS')

    def set_offset(self, val):
        self.scpi_write('VOLT:OFFS', val)

    func_to_scpi={function.Sinusoid:"SIN", 
                function.Square:'SQU',
                function.Ramp:'RAMP',
                function.Noise:'NOIS',
                function.DC:'DC'}

    def get_function(self):
        out = self.scpi_ask('FUNC')
        for key, elm in self.func_to_scpi.items():
            if is_equal(out, elm):
                return key
        raise ValueError('Unknown function {}'.format(out))
            

    def set_function(self, val):
        val = function.convert(val)
        self.scpi_write('FUNC', self.func_to_scpi[val])

