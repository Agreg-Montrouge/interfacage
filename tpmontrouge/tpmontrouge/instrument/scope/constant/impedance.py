""" Define constants for the impedance of the channel of the scope 

Example : 

  from scope.impedance import FiftyOhm, Max

  scope.ch1.impedance = FiftyOhm
  assert scope.ch1.impedance == FiftyOhm

  scope.ch1.impedance = Max
  print scope.ch1.impedance

"""

class ImpedanceError(ValueError):
    pass

class Impedance(object):
    available_impedance = []
    def __init__(self, name, value):
        self._name = name
        self._value = value
        self.available_impedance.append(self)

    def __repr__(self):
        return self._name

    def __hash__(self):
        return hash(self._name)

    def __eq__(self, other):
        if isinstance(other, str):
            return other.lower()==self._name.lower()
        return self._value.__eq__(other)

    @classmethod
    def convert(cls, val):
        if isinstance(val, cls):
            return val
        for elm in cls.available_impedance:
            if elm==val:
                return elm
        raise ImpedanceError('Value not allowed')

for binary_func_name in ['lt', 'le', 'ne', 'gt', 'ge']:
    name = '__'+binary_func_name+'__'
    setattr(Impedance, name, eval('lambda self, other:self._value.{name}(other)'.format(name=name)))

FiftyOhm = Impedance('FiftyOhm', 50)
SeventyFiveOhm = Impedance('SenventyFiveOhm', 75)
OneMegOhm = Impedance('OneMegOhm', 1E6)
Max = Impedance('Max', float('inf'))

convert = Impedance.convert
