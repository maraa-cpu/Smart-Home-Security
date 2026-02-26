from machine import Pin

class PIR:
    def __init__(self, pin_number, led_pin=None):
        self.pir = Pin(pin_number, Pin.IN)

    def motion_detected(self):
        return self.pir.value() == 1
