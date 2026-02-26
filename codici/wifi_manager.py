import network
import time
import config

class WIFIManager:
    def __init__(self):
        self.ssid = config.WIFI_SSID
        self.password = config.WIFI_PASSWORD
        self.wlan = network.WLAN(network.STA_IF)

    def connect(self, max_attempts=20):
        # Spegniamo e riaccendiamo sempre l'interfaccia per pulire lo stato interno
        if self.wlan.active():
            self.wlan.active(False)
            time.sleep_ms(200) # Pausa per permettere il reset hardware
        
        self.wlan.active(True)
        time.sleep_ms(200) 

        if not self.wlan.isconnected():
            print(f"Tentativo di connessione a: {self.ssid}")
            self.wlan.connect(self.ssid, self.password)

            attempt = 0
            while not self.wlan.isconnected() and attempt < max_attempts:
                attempt += 1
                time.sleep(0.5)

        if self.wlan.isconnected():
            print("Connessione riuscita! IP:", self.wlan.ifconfig()[0])
        else:
            print("Connessione fallita.")
            
        return self.wlan

    def is_connected(self):
        return self.wlan.isconnected()
