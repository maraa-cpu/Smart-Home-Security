import utime
from machine import Pin

class StepMotor:
    
    CW  = -1   # orario
    CCW =  1   # antiorario

    def __init__(self, in1, in2, in3, in4, delay=0.003, steps_per_rev=2048):        
        self.pins = [
            Pin(in1, Pin.OUT),
            Pin(in2, Pin.OUT),
            Pin(in3, Pin.OUT),
            Pin(in4, Pin.OUT),
        ]

        self.sequence = [
            [1, 0, 0, 1],
            [1, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 1],
        ]

        self.delay = delay
        self.steps_per_rev = steps_per_rev
        self.step_index = 0
        self._stop_flag = False

        self.release()

    def _write(self, values):
        for p, v in zip(self.pins, values):
            p.value(v)

    def stop(self):
        self._stop_flag = True

    def release(self):
        self._write([0, 0, 0, 0])

    def move_steps(self, direction, steps):
        self._stop_flag = False
        steps = int(steps)

        for _ in range(steps):
            if self._stop_flag:
                break

            self.step_index = (self.step_index + direction) % len(self.sequence)
            self._write(self.sequence[self.step_index])
            utime.sleep(self.delay)

        self.release()

    def move_turns(self, direction, turns):
        total_steps = int(turns * self.steps_per_rev)
        self.move_steps(direction, total_steps)

