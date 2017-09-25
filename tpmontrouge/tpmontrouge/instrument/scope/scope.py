from ..utils.command_tree import Node, RootNode, WithIndex, Property, IndexableProperty


class ChannelNode(Node):
    def __init__(self, parent, key):
        self.channel_name = key
        self.key = key
        self._parent = parent
           
#    @property
#    def coupling(self):
#        return self.root.get_channel_coupling(self.channel_name)

#    @coupling.setter
#    def coupling(self, val):
#        return self.root.set_channel_coupling(val, self.channel_name)

#    @property
#    def impedance(self):
#        return self.root.get_channel_impedance(self.channel_name)

#    @impedance.setter
#    def impedance(self, val):
#        return self.root.set_channel_impedance(val, self.channel_name)

    coupling = IndexableProperty('channel_coupling')
    impedance = IndexableProperty('channel_impedance')
    offset = IndexableProperty('channel_vertical_offset')
    scale = IndexableProperty('channel_vertical_scale')

    def get_waveform(self, **kwd):
        return self.root.get_channel_waveform(self.channel_name, **kwd)


class Trigger(Node):
    slope = Property('trigger_slope')
    level = Property('trigger_level')
    source = Property('trigger_source')

class Horizontal(Node):
    offset = Property('horizontal_offset')
    scale = Property('horizontal_scale')

class Scope(RootNode):
    def __init__(self, root=None):
        if root is None:
            root=self
        self._root = root

    def autoset(self):
        self.root.autoset_command()

    def start_acquisition(self):
        self.root.start_acquisition_command()


    def stop_acquisition(self):
        self.root.stop_acquisition_command()

    number_of_channel = 2
    @property
    def channel(self):
        return WithIndex(parent=self, node_class=ChannelNode)

    @property
    def channel1(self):
        return self.channel[1]

    @property
    def channel2(self):
        return self.channel[2]

    @property
    def channel3(self):
        return self.channel[3]

    @property
    def channel4(self):
        return self.channel[4]


    @property
    def trigger(self):
        return Trigger(parent=self)

    @property
    def horizontal(self):
        return Horizontal(parent=self)
