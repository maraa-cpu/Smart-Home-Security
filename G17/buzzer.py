from machine import Pin, PWM
import utime
import math

class BUZZER:
    def __init__(self, sig_pin):
        self.pwm = PWM(Pin(sig_pin, Pin.OUT))
        self.pwm.duty(0) 

        self._porta_on = False
        self._porta_last = utime.ticks_ms()
        self._porta_x = 0
        self._porta_step_ms = 10
        self._porta_duty = 512

        self._finestra_on = False
        self._finestra_last = utime.ticks_ms()
        self._finestra_state = 0       
        self._finestra_count = 0        
        self._finestra_target = 0       
        self._finestra_pausa_ms = 120
        self._finestra_duty = 512
        self._finestra_freq = 2500

    def alarm_porta(self, duty=512, step_ms=10):
        if not self._porta_on:
            self._porta_on = True
            self._porta_last = utime.ticks_ms()
            self._porta_x = 0
            self._porta_step_ms = step_ms
            self._porta_duty = duty

        if not self._porta_on:
            return

        now = utime.ticks_ms()
        if utime.ticks_diff(now, self._porta_last) >= self._porta_step_ms:
            self._porta_last = now

            sinVal = math.sin(self._porta_x * 10 * math.pi / 180)  
            toneVal = 2000 + int(sinVal * 500)                     

            self.pwm.freq(toneVal)
            self.pwm.duty(self._porta_duty)

            self._porta_x = (self._porta_x + 1) % 36

    def alarm_finestra(self, ripetizioni=8, freq=2500, duty=512, pausa_ms=120):
        if not self._finestra_on:
            self._finestra_on = True
            self._finestra_last = utime.ticks_ms()
            self._finestra_state = 0
            self._finestra_count = 0
            self._finestra_target = ripetizioni
            self._finestra_pausa_ms = pausa_ms
            self._finestra_duty = duty
            self._finestra_freq = freq

        if not self._finestra_on:
            return

        now = utime.ticks_ms()
        if utime.ticks_diff(now, self._finestra_last) >= self._finestra_pausa_ms:
            self._finestra_last = now

            if self._finestra_state == 0:
                self.pwm.freq(self._finestra_freq)
                self.pwm.duty(self._finestra_duty)
                self._finestra_state = 1
            else:
                self.pwm.duty(0)
                self._finestra_state = 0
                self._finestra_count += 1

                if self._finestra_count >= self._finestra_target:
                    self._finestra_on = False
                    self.pwm.duty(0)

    def play(self, melody, wait_ms=150, duty=300):
        self._porta_on = False
        self._finestra_on = False

        for note in melody:
            if note == 0:
                self.pwm.duty(0)
            else:
                self.pwm.freq(note)
                self.pwm.duty(duty)
            utime.sleep_ms(wait_ms)

        self.stop()

    def stop(self):

        self._porta_on = False
        self._finestra_on = False
        self.pwm.duty(0)


