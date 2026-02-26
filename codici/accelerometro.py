from machine import Pin, I2C
import utime
import math

class Accelerometro:
    MPU_ADDR = 0x68
    PWR_MGMT_1 = 0x6B
    ACCEL_XOUT_H = 0x3B

    def __init__(self, scl_pin=22, sda_pin=21, soglia=1):
        self.soglia = soglia
        self.i2c = I2C(0, scl=Pin(scl_pin), sda=Pin(sda_pin))
        self.i2c.writeto_mem(self.MPU_ADDR, self.PWR_MGMT_1, b'\x00')

    def set_soglia(self, nuova_soglia):
        """Aggiorna la soglia da Node-RED"""
        try:
            self.soglia = float(nuova_soglia)
            print("Nuova soglia accelerometro:", self.soglia)
        except:
            print("ERRORE: soglia non valida:", nuova_soglia)
    
    def _read_raw_data(self, reg):
        high = self.i2c.readfrom_mem(self.MPU_ADDR, reg, 1)[0]
        low  = self.i2c.readfrom_mem(self.MPU_ADDR, reg+1, 1)[0]
        value = (high << 8) | low
        if value >= 32768:
            value -= 65536
        return value

    def read_acceleration(self):
        acc_x = self._read_raw_data(self.ACCEL_XOUT_H)
        acc_y = self._read_raw_data(self.ACCEL_XOUT_H + 2)
        acc_z = self._read_raw_data(self.ACCEL_XOUT_H + 4)

        ax = acc_x / 16384
        ay = acc_y / 16384
        az = acc_z / 16384

        return {"x": ax, "y": ay, "z": az}

    def is_alarm(self):
        a = self.read_acceleration()

        if abs(a["x"]) > self.soglia:
            return True
        if abs(a["y"]) > self.soglia:
            return True
        if abs(a["z"]) > self.soglia:
            return True

        return False
