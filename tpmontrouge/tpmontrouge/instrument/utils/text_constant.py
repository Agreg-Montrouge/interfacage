class TextConstantError(ValueError):
    pass

class TextConstantMetaclass(type):
    def __init__(cls, name, *args, **kwd):
        if name!='TextConstant':
            cls._available = []

class TextConstant(metaclass=TextConstantMetaclass):
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
        raise TextConstantError('Value not allowed')

    def __eq__(self, other):
        if isinstance(other, str):
            other = self.convert(other)
        if not hasattr(other, '_name'):
            return NotImplemented
        return self._name == other._name

    def __repr__(self):
        return '{cls_name}("{name}")'.format(cls_name=self.__class__.__name__, name=self._name)

    def __str__(self):
        return self._name

