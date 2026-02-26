from machine import Pin

class SensoreMagnetico:
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.IN, Pin.PULL_UP)

    def is_open(self):
        return self.pin.value() == 1

