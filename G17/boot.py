import machine
import time
import config

from  wifi_manager import WIFIManager

# --- WIFI CONNECTION ---
wifi = WIFIManager()
wlan = wifi.connect()
