import machine
import utime

class Button:

    def __init__(self, pin, pull=machine.Pin.PULL_UP):
        self.pin = machine.Pin(pin, machine.Pin.IN, pull)
        self._last_check = utime.ticks_ms()
        self._debounce_ms = 50

    def is_pressed(self):
        if self.pin.value() == 0:
            # piccolo debounce
            utime.sleep_ms(self._debounce_ms)
            return self.pin.value() == 0
        return False
