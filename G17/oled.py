from machine import Pin, I2C
import ssd1306
import framebuf

class OLEDDisplay:
    def __init__(self, width=128, height=64, scl_pin=22, sda_pin=21):
        self.width = width
        self.height = height
        self.i2c = I2C(0, scl=Pin(scl_pin), sda=Pin(sda_pin))
        self.oled = ssd1306.SSD1306_I2C(self.width, self.height, self.i2c)
        self.clear()

    def clear(self):
        self.oled.fill(0)
        self.oled.show()

    def show_text(self, text, x=0, y=0):
        self.oled.text(text, x, y)
        self.oled.show()

    def show_logo(self, logo_bytes):
        fb = framebuf.FrameBuffer(logo_bytes, self.width, self.height, framebuf.MONO_HLSB)
        self.oled.fill(0)
        self.oled.blit(fb, 0, 0)
        self.oled.show()

    # ================= SCHERMATE PERSONALIZZATE =================

    def standby_scr(self):
        self.clear()
        self.oled.text("Sistema OFF", 0, 0)
        self.oled.text("Inserisci codice", 0, 16)
        self.oled.text("per armare", 0, 26)
        self.oled.show()

    def show_code_scr(self, codice, msg=None):
        self.clear()
        self.oled.text("Inserisci codice", 0, 0)
        self.oled.text("Codice:", 0, 16)
        self.oled.text("*" * len(codice), 60, 16)

        self.oled.text("# Conferma", 0, 36)
        self.oled.text("* Annulla", 0, 46)

        if msg:
            self.oled.text(msg, 0, 56)

        self.oled.show()

    def porta_aperta_scr(self):
        self.clear()
        self.oled.text("PORTA APERTA!", 0, 16)
        self.oled.show()

    def countdown_scr(self, left, codice, modalita_notte, tempo_totale):
        self.oled.fill(0)
        self.oled.text("ENTRATA", 0, 0)
        self.oled.text("NOTTE" if modalita_notte else "TOTALE", 70, 0)
        self.oled.hline(0, 10, 128, 1)

        self.oled.text("{}s".format(left), 0, 18)

        w = int((left / tempo_totale) * 120) if tempo_totale > 0 else 0
        self.oled.rect(0, 30, 122, 10, 1)
        self.oled.fill_rect(1, 31, w, 8, 1)

        self.oled.text("Codice:", 0, 48)
        self.oled.text("*" * len(codice), 60, 48)
        self.oled.show()


    def uscita_scr(self, left, tempo_totale):
        self.oled.fill(0)
        self.oled.text("Tempo di USCITA", 0, 0)
        self.oled.hline(0, 10, 128, 1)

        self.oled.text("{}s".format(left), 0, 18)

        w = int((left / tempo_totale) * 120) if tempo_totale > 0 else 0
        self.oled.rect(0, 30, 122, 10, 1)
        self.oled.fill_rect(1, 31, w, 8, 1)

        self.oled.text("Esci e chiudi", 0, 48)
        self.oled.show()

    def bentornato_scr(self):
        self.clear()
        self.oled.text("BENTORNATO!", 0, 24)
        self.oled.show()

    def notte_disattivata_scr(self):
        self.clear()
        self.oled.text("Modalita NOTTE", 0, 16)
        self.oled.text("DISATTIVATA", 0, 26)
        self.oled.text("Buongiorno", 0, 46)
        self.oled.show()

    def notte_attivata_scr(self):
        self.clear()
        self.oled.text("NOTTE ATTIVA", 0, 8)
        self.oled.text("Casa protetta", 0, 24)
        self.oled.text("Zzz...", 0, 44)
        self.oled.show()
    
    def tenda_chiusura_scr(self):
        self.clear()
        self.oled.text("Chiusura tenda", 0, 16)
        self.oled.text("in corso...", 0, 26)
        self.oled.show()

    def tenda_apertura_scr(self):
        self.clear()
        self.oled.text("Apertura tenda", 0, 16)
        self.oled.text("in corso...", 0, 26)
        self.oled.show()

    def allarme_scr(self, codice, titolo="ALLARME", msg=None):
        self.clear()

        self.oled.text(titolo, 0, 0)
        self.oled.text("Inserisci codice", 0, 16)

        self.oled.text("Codice:", 0, 32)
        self.oled.text("*" * len(codice), 60, 32)

        if msg:
            self.oled.text(msg, 0, 40)

        self.oled.text("# Conferma", 0, 52)
        self.oled.text("* Annulla", 0, 60)

        self.oled.show()

    def scelta_modalita_scr(self):
        self.oled.fill(0)
        self.oled.text("Seleziona modo", 0, 0)
        self.oled.hline(0, 10, 128, 1)

        self.oled.rect(0, 16, 128, 18, 1)
        self.oled.text("A  NOTTE", 8, 22)

        self.oled.rect(0, 38, 128, 18, 1)
        self.oled.text("B  TOTALE", 8, 44)

        self.oled.text("* ANNULLA", 0, 56)
        self.oled.show()




