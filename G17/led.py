from machine import Pin
import utime

class LED:
    def __init__(self, pin, active_high=True):
        self.led = Pin(pin, Pin.OUT)
        self.active_high = active_high

        self.off()
        
        self._last_toggle = 0
        self._state = False

    def on(self):
        self.led.value(1 if self.active_high else 0)

    def off(self):
        self.led.value(0 if self.active_high else 1)

    def blink_once(self, duration_ms=200):
        self.on()
        utime.sleep_ms(duration_ms)
        self.off()
        utime.sleep_ms(duration_ms)

    def blink(self, interval_ms=200):
        now = utime.ticks_ms()
        if utime.ticks_diff(now, self._last_toggle) > interval_ms:
            self._last_toggle = now
            self._state = not self._state

            if self._state:
                self.on()
            else:
                self.off()

