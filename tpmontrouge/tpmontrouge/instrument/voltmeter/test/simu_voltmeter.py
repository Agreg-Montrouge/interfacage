from time import sleep

class VoltmeterSimulation(object):
    x = 0
    def on_command(self):
        self._last_command = "on"

    def off_command(self):
        self._last_command = "off"

    def get_value(self):
        self.x += .1
        sleep(0.012)
        return self.x
