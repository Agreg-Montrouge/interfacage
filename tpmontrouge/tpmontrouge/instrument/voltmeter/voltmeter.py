from ..utils.command_tree import Node, RootNode, Property

class Voltmeter(RootNode):
    def __init__(self, root=None):
        if root is None:
            root=self
        self._root = root

    def get_value(self):
        raise Exception("You should implement the 'get_value' method")

#    value = Property("frequency")
#    amplitude = Property("amplitude")
#    function = Property("function")
#    offset = Property("offset")

#    def on(self):
#        self.root.on_command()

#    def off(self):
#        self.root.off_command()


