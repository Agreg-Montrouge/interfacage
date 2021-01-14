from ..utils.command_tree import Node, RootNode, WithIndex, Property, IndexableProperty

class GBF(RootNode):
    __slots__ = ['_root']
    @classmethod
    def get_simulated_device(cls):
        from .test.simu_gbf import GBFSimulation
        return cls(root = GBFSimulation())

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

