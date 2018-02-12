class WithIndex(object):
    def __init__(self, parent, node_class, index_range=None):
        self._parent = parent
        self._node_class = node_class
        self._index_range = index_range
        
    def __getitem__(self, key):
        if self._index_range is not None:
            if key not in self._index_range:
                raise IndexError('The value of the index should be in {}'.format(self._index_range))
        return self._node_class(parent=self._parent, key=key)


class Node(object):
    def __init__(self, parent):
        self._parent = parent

    @property
    def root(self):
        return self._parent.root

class RootNode(object):
    @property
    def root(self):
        return self._root

class Property(object):
    def __init__(self, name):
        self._name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance.root, 'get_'+self._name)()

    def __set__(self, instance, value):
        getattr(instance.root, 'set_'+self._name)(value)


class IndexableProperty(object):
    def __init__(self, name):
        self._name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance.root, 'get_'+self._name)(instance.key)

    def __set__(self, instance, value):
        getattr(instance.root, 'set_'+self._name)(value, instance.key)



