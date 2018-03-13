from ..utils.command_tree import Node, RootNode, Property

class Voltmeter(RootNode):
    def __init__(self, root=None, name=''):
        self.name = name
        if root is None:
            root=self
        self._root = root

    def get_value(self):
        if self.root!=self:
            return self.root.get_value()

    def get_one_point(self):
        return self.get_value()

#    value = Property("frequency")
#    amplitude = Property("amplitude")
#    function = Property("function")
#    offset = Property("offset")

#    def on(self):
#        self.root.on_command()

#    def off(self):
#        self.root.off_command()


