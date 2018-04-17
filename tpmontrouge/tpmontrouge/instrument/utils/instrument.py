

class Instrument(object):
    def __init__(self, inst):
        """ Initialise the instrument

        argument : 
            inst : should be a visa string or an object with write and ask method

        """
        if not hasattr(inst, 'write'): 
            if isinstance(inst, str):
                if visa is not None:
                    rm = visa.ResourceManager()
                    inst = rm.open_resource(inst)
                else:
                    raise Exception('Visa is not install on your system')
            else:
                raise ValueError('First argument should be a string or an instrument')
        self._inst = inst

    _last_command = None
    def write(self, cmd):
        self._last_command=cmd
        return self._inst.write(cmd)

    def ask(self, cmd):
        return self._inst.ask(cmd)

    def ask_raw(self, cmd):
        if hasattr(self._inst, 'read_raw'):
            self.write(cmd)
            return self._inst.read_raw()[:-1]
        else:
            return self._inst.ask(cmd)

    def scpi_write(self, cmd, *args):
        return self.write(cmd + ' '+','.join(map(str, args)))

    def scpi_ask(self, cmd):
        return self.ask(cmd if cmd.endswith('?') else cmd + '?').strip()

    def scpi_ask_for_float(self, cmd):
        return float(self.scpi_ask(cmd))

    @classmethod
    def add_class_to_manufacturer(cls, model_name):
        cls.manufacturer.add_model(model_name, cls)

    @property
    def idn(self):
        out = self.ask('*IDN?')
        return out.strip().split(',')

    @property
    def maunfacturer(self):
        return self.idn[0]

    @property
    def model_number(self):
        return self.idn[1]

    @property
    def serial_number(self):
        return self.idn[2]


class FakeSCPI(object):
    _record = {}
    def write(self, val):
        if ' ' in val:
            cmd, vals = val.split(' ')
            self._record[cmd] = vals
#            print('WRITE', cmd, vals)

    def ask(self, val):
        assert val[-1]=='?'
        out = self._record.get(val[:-1], '')
#        print('ASK', val,'...', out)
        return out


