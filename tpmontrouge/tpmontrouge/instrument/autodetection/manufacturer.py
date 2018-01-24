import re
from warnings import warn

class ListOfManufacturer(object):
    def __init__(self):
        self._list_of_manufacturer = []

    def add_manufacturer(self, name, instance):
        self._list_of_manufacturer.append((name, instance))

    def __str__(self):
        return '\n'.join(["{name} : {instance}".format(name=name, instance=instance)
                    for name, instance in self._list_of_manufacturer])

    def get(self, val):
        for name, instance in self._list_of_manufacturer:
            if name.lower()==val.lower():
                return instance
        return None

list_of_manufacturer = ListOfManufacturer()

class Manufacturer(object):
    def __init__(self, name):
        self._name = name
        self._list_of_model = []

    def add_model(self, model_name, model_class):
        """ Add a model

        model_name may be a regulat expression : 
            "DSO\d+" or "DSO.*"
        Add at the begining of the list
        """
        self._list_of_model.insert(0, (model_name, model_class))

    def get_model_class(self, val):
        for model_name, model_class in self._list_of_model:
            if re.match(model_name, val, re.IGNORECASE):
                return model_class
        warn('Unkwnown model {} for {}'.format(val, self))


    def add_to_list_of_manufacturer(self, name=None):
        name = name or self._name
        list_of_manufacturer.add_manufacturer(name, self)

    def __repr__(self):
        return 'Manufacturer({})'.format(self._name)

tektronix = Manufacturer('Tektronix')
tektronix.add_to_list_of_manufacturer()

agilent_technologies = Manufacturer('Agilent')
agilent_technologies.add_to_list_of_manufacturer('Agilent Technologies')
keysight = agilent_technologies

metrix = Manufacturer('Metrix')
metrix.add_to_list_of_manufacturer()

