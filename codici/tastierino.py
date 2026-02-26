from machine import Pin
import utime

class Tastierino:
    def __init__(self, row_pins, col_pins, key_map):
        self.row_pins = row_pins
        self.col_pins = col_pins
        self.key_map = key_map

        self.rows = [Pin(pin, Pin.IN, Pin.PULL_UP) for pin in self.row_pins]
        self.cols = [Pin(pin, Pin.OUT) for pin in self.col_pins]

        for c in self.cols:
            c.value(1)

    def scan_key(self):
        for c_idx, c in enumerate(self.cols):
            c.value(0)
            utime.sleep_us(50)

            for r_idx, r in enumerate(self.rows):
                if r.value() == 0:  
                    key = self.key_map[r_idx][c_idx]

                    while r.value() == 0:
                        utime.sleep_ms(10)

                    c.value(1)
                    return key

            c.value(1)

        return None

