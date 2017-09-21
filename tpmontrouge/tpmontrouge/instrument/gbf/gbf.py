from ..utils.command_tree import Node, RootNode, WithIndex, Property, IndexableProperty

class GBF(RootNode):
    def __init__(self, root=None):
        if root is None:
            root=self
        self._root = root

    frequency = Property("frequency")
    amplitude = Property("amplitude")
    function = Property("function")
    offset = Property("offset")

    def on(self):
        self.root.on_command()

    def off(self):
        self.root.off_command()

