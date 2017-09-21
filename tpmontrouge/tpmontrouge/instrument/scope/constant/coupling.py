""" Define constants for the coupling of a scope channel 

Example : 

  from scope import coupling

  print(coupling.AC)

"""

class CouplingError(ValueError):
    pass

class Coupling(object):
    _available = []
    def __init__(self, name):
        self._name = name
        self._available.append(self)

    def __repr__(self):
        return self._name

    def __hash__(self):
        return hash(self._name)

    @classmethod
    def convert(cls, val):
        if isinstance(val, cls):
            return val
        for elm in cls._available:
            if elm._name.lower()==val.lower():
                return elm
        raise CouplingError('Value not allowed')

    def __eq__(self, other):
        if isinstance(other, str):
            other = self.convert(other)
        if not hasattr(other, '_name'):
            return NotImplemented
        return self._name == other._name

AC = Coupling('AC')
DC = Coupling('DC')
GND = Coupling('GND')


convert = Coupling.convert
