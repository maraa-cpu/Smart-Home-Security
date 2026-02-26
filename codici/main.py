import utime
import machine
import boot

from wifi_manager import WIFIManager
from mqtt_manager import MQTTManager
from stepmotor import StepMotor
from tastierino import Tastierino
from sensore_magnetico import SensoreMagnetico
from pir import PIR
from led import LED
from accelerometro import Accelerometro
from oled import OLEDDisplay
from buzzer import BUZZER
from button import Button
from config import (TEMPO_COUNTDOWN, TEMPO_USCITA, GIRI_CHIUSURA, GIRI_APERTURA, CODICE_CORRETTO, MELODIA_BENVENUTO_LUNGA, MELODIA_ERRORE_CODICE, LOGO)

# STATI
STANDBY = 0
INSERITO = 1
PREALLARME = 2
COUNTDOWN = 3
ALLARME = 4
SCELTA_MODALITA = 5
USCITA = 6

# Tipi di allarme
ALLARME_PORTA = 0
ALLARME_FINESTRA = 1


def main():
    oled = OLEDDisplay(width=128, height=64, scl_pin=22, sda_pin=21)
    buzzer = BUZZER(sig_pin=32)
    led = LED(pin=33)
    pir = PIR(pin_number=35)
    porta = SensoreMagnetico(pin=2)
    accelerometro = Accelerometro(scl_pin=22, sda_pin=21, soglia=1.2)
    motore = StepMotor(in1=5, in2=12, in3=13, in4=14, delay=0.003)
    reset_button = Button(pin=4)


    ROW = [16, 17, 18, 19]
    COL = [23, 25, 26, 27]
    KEY_MAP = [
        ['1', '2', '3', 'A'],
        ['4', '5', '6', 'B'],
        ['7', '8', '9', 'C'],
        ['*', '0', '#', 'D']
    ]
    tastiera = Tastierino(ROW, COL, KEY_MAP)

    # VARIABILI DI STATO
    stato = STANDBY
    allarme_attivo = False
    tipo_allarme = None
    last_stato = -1  # Per inviare MQTT solo al cambio

    modalita_notte = False   # False = totale, True = notte
    tenda_chiusa = False     # False = tenda su, True = tenda giù

    codice = ""
    errori = 0
    timer_ingresso = 0
    timer_uscita = 0

    wifi = WIFIManager()
    wlan = wifi.connect()

    mqtt = MQTTManager()
    has_mqtt = mqtt.connect()
    
    if has_mqtt:
        # Avvisa Node-RED che l'ESP è ripartito
        mqtt.client.publish(b"casa/caveau/status", b"REBOOT")

    last_telemetry_time = utime.ticks_ms()

    # LOGO INIZIALE + standby
    oled.clear()
    oled.show_logo(LOGO)
    utime.sleep_ms(5000)
    oled.standby_scr()
    
    # --- PUBBLICA STATO TENDA AL BOOT ---
    if tenda_chiusa:
        mqtt.client.publish(b"casa/caveau/telemetry/tenda", b"chiusa")
    else:
        mqtt.client.publish(b"casa/caveau/telemetry/tenda", b"aperta")
    

    # LOOP PRINCIPALE
    while True:
        now = utime.ticks_ms()
        
        # ================= RESET GESTITO =================
        if reset_button.is_pressed():      # pulsante premuto (già debounciato)
            print("DEBUG: Reset premuto")
            if tenda_chiusa: 
                mqtt.client.publish(b"casa/caveau/telemetry/tenda", b"apertura")
                
                oled.tenda_apertura_scr()
                motore.move_turns(StepMotor.CCW, GIRI_APERTURA)
                tenda_chiusa = False
                mqtt.client.publish(b"casa/caveau/telemetry/tenda", b"aperta")
            utime.sleep_ms(300)
            machine.reset()
        
        # --- MQTT ---
        if has_mqtt:
            mqtt.check_msg()

        # Pubblica stato solo quando cambia
        if stato != last_stato:
            state_str = "UNKNOWN"
            if stato == STANDBY:
                state_str = "disarmed"
            elif stato == INSERITO:
                state_str = "night" if modalita_notte else "total"
            elif stato == PREALLARME:
                state_str = "PREALLARME"
            elif stato == COUNTDOWN:
                state_str = "COUNTDOWN"
            elif stato == ALLARME:
                if tipo_allarme == ALLARME_PORTA:
                    state_str = "ALLARME_PORTA"
                elif tipo_allarme == ALLARME_FINESTRA:
                    state_str = "ALLARME_FINESTRA"
                else:
                    state_str = "ALLARME"
            elif stato == SCELTA_MODALITA:
                state_str = "SCELTA_MODALITA"
            elif stato == USCITA:
                state_str = "USCITA"

            mqtt.publish(state_str)
            last_stato = stato

        cmd_received = mqtt.get_last_command()
        if cmd_received:
            cmd = cmd_received

            # --- GESTIONE SOGLIA ACCELEROMETRO ---
            if cmd.startswith("SOG="):
                valore = cmd.split("=")[1]
                accelerometro.set_soglia(valore)
                continue
            
            # --- COMANDO APERTURA/CHIUSURA FINESTRA ---
            if cmd.startswith("FINESTRA="):

                # Blocco totale se NON sei in modalità DISARMED
                if stato != STANDBY:
                    print("DEBUG: Ignoro comando finestra, sistema non disarmato")
                    continue

                # Apertura finestra
                if cmd == "FINESTRA=OPEN":
                    if tenda_chiusa:

                        # 1) Notifica inizio apertura
                        mqtt.client.publish(b"casa/caveau/telemetry/tenda", b"apertura")

                        oled.tenda_apertura_scr()

                        # 2) Movimento fisico
                        motore.move_turns(StepMotor.CCW, GIRI_APERTURA)
                        tenda_chiusa = False

                        # 3) Notifica fine apertura
                        mqtt.client.publish(b"casa/caveau/telemetry/tenda", b"aperta")

                        oled.standby_scr()
                        
                    else:
                        print("DEBUG: Finestra già aperta")
                    continue

                # Chiusura finestra
                if cmd == "FINESTRA=CLOSE":
                    if not tenda_chiusa:

                        # 1) Notifica inizio chiusura
                        mqtt.client.publish(b"casa/caveau/telemetry/tenda", b"chiusura")

                        oled.tenda_chiusura_scr()

                        # 2) Movimento fisico
                        motore.move_turns(StepMotor.CW, GIRI_CHIUSURA)
                        tenda_chiusa = True

                        # 3) Notifica fine chiusura
                        mqtt.client.publish(b"casa/caveau/telemetry/tenda", b"chiusa")

                        oled.standby_scr()
                    else:
                        print("DEBUG: Finestra già chiusa")
                    continue
                
                
            if cmd == "TENDACHIUSA_SOFTWARE":
                tenda_chiusa = True
                continue

            if cmd == "TENDAAPERTA_SOFTWARE":
                tenda_chiusa = False
                continue

            # --- DISARMO REMOTO ---
            if cmd in ("OPEN", "DISATTIVA", "DISATTIVO", "DISARMED"):
                if stato in (ALLARME, COUNTDOWN, PREALLARME, INSERITO):
                    if stato == ALLARME:
                        buzzer.stop()
                        led.off()
                        allarme_attivo = False
                        tipo_allarme = None

                    if tenda_chiusa:

                        # 1) Notifica inizio apertura
                        mqtt.client.publish(b"casa/caveau/telemetry/tenda", b"apertura")

                        oled.tenda_apertura_scr()

                        # 2) Movimento fisico
                        motore.move_turns(StepMotor.CCW, GIRI_APERTURA)
                        tenda_chiusa = False
                        modalita_notte = False

                        # 3) Notifica fine apertura
                        mqtt.client.publish(b"casa/caveau/telemetry/tenda", b"aperta")
                        oled.notte_disattivata_scr()
                        utime.sleep_ms(1200)
                    else:
                        modalita_notte = False
                        oled.bentornato_scr()
                        buzzer.play(MELODIA_BENVENUTO_LUNGA)
                        utime.sleep_ms(1000)

                    oled.clear()
                    oled.show_logo(LOGO)
                    utime.sleep_ms(1000)
                    stato = STANDBY
                    oled.standby_scr()
                    codice = ""
                continue

            # --- ATTIVA NOTTE REMOTO ---
            if cmd in ("NOTTE", "CLOSE", "ATTIVA", "NIGHT"):
                if stato in (STANDBY, SCELTA_MODALITA):
                    modalita_notte = True

                    if not tenda_chiusa:

                        # 1) Notifica inizio chiusura
                        mqtt.client.publish(b"casa/caveau/telemetry/tenda", b"chiusura")

                        oled.tenda_chiusura_scr()

                        # 2) Movimento fisico
                        motore.move_turns(StepMotor.CW, GIRI_CHIUSURA)
                        tenda_chiusa = True

                        # 3) Notifica fine chiusura
                        mqtt.client.publish(b"casa/caveau/telemetry/tenda", b"chiusa")

                    oled.clear()
                    oled.show_text("Allarme INSERITO", 0, 0)
                    oled.show_text("Modalita:", 0, 16)
                    oled.show_text("NOTTE", 0, 26)
                    utime.sleep_ms(700)
                    stato = INSERITO
                continue

            # --- ATTIVA TOTALE REMOTO ---
            if cmd in ("GIORNO", "TOTAL", "TOTALE"):
                if stato in (STANDBY, SCELTA_MODALITA):
                    modalita_notte = False
                    timer_uscita = utime.ticks_ms()
                    stato = USCITA
                    oled.uscita_scr(TEMPO_USCITA, TEMPO_USCITA)
                continue

        # --- LETTURA SENSORI ---
        porta_aperta = porta.is_open()
        pir_ok = pir.motion_detected()
        acc_ok = accelerometro.is_alarm()

        # --- TASTIERINO ---
        tasto = tastiera.scan_key()

        if tasto:

            # ================== GESTIONE TASTI IN STATO ALLARME ==================
            if stato == ALLARME:
                # Cifre del codice durante ALLARME
                if tasto in "0123456789" and len(codice) < 4:
                    codice += tasto
                    oled.show_code_scr(codice)
                    continue

                # Cancella codice
                if tasto == "*":
                    codice = ""
                    oled.show_code_scr(codice, "Inserimento cancellato")
                    utime.sleep_ms(1000)
                    oled.show_code_scr(codice)
                    continue

                # Conferma codice con #
                if tasto == "#":
                    if codice == CODICE_CORRETTO:
                        # Disarmo da ALLARME (il tuo codice identico a prima)
                        buzzer.stop()
                        led.off()
                        allarme_attivo = False
                        tipo_allarme = None

                        if tenda_chiusa:
                            oled.tenda_apertura_scr()
                            motore.move_turns(StepMotor.CCW, GIRI_APERTURA)
                            tenda_chiusa = False
                            modalita_notte = False
                            oled.notte_disattivata_scr()
                            utime.sleep_ms(1200)
                        else:
                            modalita_notte = False
                            oled.bentornato_scr()
                            buzzer.play(MELODIA_BENVENUTO_LUNGA)
                            utime.sleep_ms(1000)

                        oled.clear()
                        oled.show_logo(LOGO)
                        utime.sleep_ms(1000)

                        stato = STANDBY
                        oled.standby_scr()
                        codice = ""
                    else:
                        # Codice errato in ALLARME
                        errori += 1
                        buzzer.play(MELODIA_ERRORE_CODICE)

                        oled.clear()
                        oled.show_text("CODICE ERRATO!", 0, 25)
                        oled.show_text("Riprova", 0, 35)
                        utime.sleep_ms(1500)

                        codice = ""
                        oled.show_code_scr(codice)

                    continue
                # Se sei in ALLARME e premi altri tasti (es. A,B,C,D), li ignoriamo
                continue
            # ================== FINE BLOCCO STATO ALLARME ==================

            # --- SCELTA MODALITA' ---
            if stato == SCELTA_MODALITA:
                if tasto == "A":
                    # Modalità NOTTE
                    modalita_notte = True
                    if not tenda_chiusa:
                        # 1) Notifica inizio chiusura
                        mqtt.client.publish(b"casa/caveau/telemetry/tenda", b"chiusura")

                        oled.tenda_chiusura_scr()

                        # 2) Movimento fisico
                        motore.move_turns(StepMotor.CW, GIRI_CHIUSURA)
                        tenda_chiusa = True

                        # 3) Notifica fine chiusura
                        mqtt.client.publish(b"casa/caveau/telemetry/tenda", b"chiusa")

                    oled.clear()
                    oled.show_text("Allarme INSERITO", 0, 0)
                    oled.show_text("Modalita:", 0, 16)
                    oled.show_text("NOTTE", 0, 26)
                    utime.sleep_ms(700)
                    stato = INSERITO

                elif tasto == "B":
                    # Modalità TOTALE: tempo di uscita
                    modalita_notte = False
                    timer_uscita = utime.ticks_ms()
                    stato = USCITA
                    oled.uscita_scr(TEMPO_USCITA, TEMPO_USCITA)

                elif tasto == "*":
                    # Annulla: torna in STANDBY
                    stato = STANDBY
                    oled.standby_scr()

                codice = ""
                continue

            # --- Tasto * = cancella il codice digitato (altri stati) ---
            if tasto == "*":
                codice = ""
                oled.show_code_scr(codice, "Inserimento cancellato")
                utime.sleep_ms(1000)
                oled.show_code_scr(codice)
                continue

            # --- Cifre codice (altri stati) ---
            if tasto in "0123456789" and len(codice) < 4:
                codice += tasto
                oled.show_code_scr(codice)
                continue

            # --- Tasto # = conferma codice (altri stati) ---
            if tasto == "#":
                if codice == CODICE_CORRETTO:
                    # 1) Disattivo da ALLARME non ci arriva più qui,
                    #    perché ALLARME è gestito sopra

                    # 2) Da STANDBY : vado a scelta modalità
                    if stato == STANDBY:
                        stato = SCELTA_MODALITA
                        codice = ""
                        oled.scelta_modalita_scr()
                        continue

                    # 3) Disattivo quando l'allarme è INSERITO (notte o totale)
                    if stato in (INSERITO, PREALLARME):
                        # stessa logica del disarmo remoto
                        if tenda_chiusa:
                            mqtt.client.publish(b"casa/caveau/telemetry/tenda", b"apertura")
                            oled.tenda_apertura_scr()
                            motore.move_turns(StepMotor.CCW, GIRI_APERTURA)
                            tenda_chiusa = False
                            modalita_notte = False
                            mqtt.client.publish(b"casa/caveau/telemetry/tenda", b"aperta")
                            oled.notte_disattivata_scr()
                            utime.sleep_ms(1200)
                        else:
                            modalita_notte = False
                            oled.bentornato_scr()
                            buzzer.play(MELODIA_BENVENUTO_LUNGA)
                            utime.sleep_ms(1000)

                        oled.clear()
                        oled.show_logo(LOGO)
                        utime.sleep_ms(1000)

                        stato = STANDBY
                        oled.standby_scr()
                        codice = ""
                        continue

                    # 4) Disattivo durante COUNTDOWN
                    if stato == COUNTDOWN:
                        if tenda_chiusa:
                            oled.tenda_apertura_scr()
                            motore.move_turns(StepMotor.CCW, GIRI_APERTURA)
                            tenda_chiusa = False
                            modalita_notte = False
                            oled.notte_disattivata_scr()
                            utime.sleep_ms(1200)
                        else:
                            modalita_notte = False
                            oled.bentornato_scr()
                            buzzer.play(MELODIA_BENVENUTO_LUNGA)
                            utime.sleep_ms(1000)

                        oled.clear()
                        oled.show_logo(LOGO)
                        utime.sleep_ms(1000)

                        stato = STANDBY
                        oled.standby_scr()
                        codice = ""
                        continue

                else:
                    # CODICE ERRATO (non in ALLARME)
                    errori += 1
                    buzzer.play(MELODIA_ERRORE_CODICE)

                    oled.clear()
                    oled.show_text("CODICE ERRATO!", 0, 25)
                    oled.show_text("Riprova", 0, 35)
                    utime.sleep_ms(1500)

                    if stato == COUNTDOWN and errori >= 2:
                        stato = ALLARME
                        codice = ""
                        continue

                    codice = ""
                    oled.show_code_scr(codice)
                    continue

        # ------------------- LOGICA ANTIFURTO -------------------
        if stato == INSERITO:

            # Allarme FINESTRA: accelerometro : scatta subito
            if acc_ok:
                tipo_allarme = ALLARME_FINESTRA
                allarme_attivo = False
                stato = ALLARME
                continue

            # Porta aperta
            if porta_aperta:
                tipo_allarme = ALLARME_PORTA

                if modalita_notte:
                    # In NOTTE: allarme immediato
                    stato = ALLARME
                else:
                    # In TOTALE: preallarme
                    stato = PREALLARME
                    oled.porta_aperta_scr()
                continue

        if stato == PREALLARME:
            # In modalità NOTTE : niente PIR, parte subito l'allarme
            if modalita_notte:
                stato = ALLARME
                allarme_attivo = False
                continue

            # In modalità totale : rilevo il PIR
            if pir_ok:
                stato = COUNTDOWN
                timer_ingresso = utime.ticks_ms()
                errori = 0
                codice = ""
                oled.countdown_scr(TEMPO_COUNTDOWN, codice, modalita_notte, TEMPO_COUNTDOWN)
                continue

        if stato == USCITA:
            delta = utime.ticks_diff(utime.ticks_ms(), timer_uscita) // 1000
            left = TEMPO_USCITA - delta
            if left < 0:
                left = 0

            oled.uscita_scr(left, TEMPO_USCITA)

            if left == 0:
                oled.clear()
                oled.show_text("Allarme INSERITO", 0, 0)
                oled.show_text("Modalita:", 0, 16)
                oled.show_text("TOTALE", 0, 26)
                utime.sleep_ms(700)
                stato = INSERITO

        if stato == COUNTDOWN:
            delta = utime.ticks_diff(utime.ticks_ms(), timer_ingresso) // 1000
            left = TEMPO_COUNTDOWN - delta
            if left < 0:
                left = 0

            oled.countdown_scr(left, codice, modalita_notte, TEMPO_COUNTDOWN)

            if left == 0:
                stato = ALLARME
                continue

        if stato == ALLARME:
            if not allarme_attivo:
                allarme_attivo = True
                codice = ""
                if not tipo_allarme:
                    tipo_allarme = ALLARME_PORTA

            led.blink(60)

            if tipo_allarme == ALLARME_PORTA:
                buzzer.alarm_porta()
                oled.allarme_scr(codice, "ALLARME PORTA")
            elif tipo_allarme == ALLARME_FINESTRA:
                buzzer.alarm_finestra()
                oled.allarme_scr(codice, "ALLARME FINESTRA")
            else:
                buzzer.alarm_porta()
                oled.allarme_scr(codice, "ALLARME")

        # --- TELEMETRIA WIFI NODERED ---
        if utime.ticks_diff(now, last_telemetry_time) > 2000:
            last_telemetry_time = now
            wlan = boot.wlan
            rssi = wlan.status('rssi')
            mqtt.client.publish(b"casa/caveau/telemetry/wifi", str(rssi))
            
        utime.sleep_ms(30)

main()



