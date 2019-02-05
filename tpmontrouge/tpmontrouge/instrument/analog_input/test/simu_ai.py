
from numpy.random import rand

import threading
from time import sleep
from queue import Queue

from ..analog_input import AnalogInput

class RawInterface(threading.Thread):
    def __init__(self, sample_rate, block_size, N_block):
        self._block_size = block_size
        self._N_block = N_block
        self._dt = block_size/sample_rate
        self.queue = Queue()
        self.want_to_stop = False
        super(RawInterface, self).__init__()

    def run(self):
        while self.want_to_stop==False:
            sleep(self._dt)
            self.queue.put(rand(self._block_size))
    
    def stop(self):
        self.want_to_stop = True
    
class AnalogInputThreadSimulation(AnalogInput):
    def __init__(self, name):
        self.name = name

    def start(self, channel_list, sample_rate, block_size, N_block):
        self._channel_list = channel_list
        self._raw_interf = RawInterface(sample_rate, block_size, N_block)
        self._raw_interf.start()

    def get_one_block(self):
        return {key:self._raw_interf.queue.get() for key in self._channel_list}

    def stop(self):
        self._raw_interf.stop()
            

class AIInterface(object):
    def __init__(self, name):
        self.name = name

    def start(self, sample_rate, block_size, N_block):
        self._block_size = block_size
        self._N_block = N_block

    def get_one_block(self):
        return rand(self._block_size)

    def stop(self):
        pass


