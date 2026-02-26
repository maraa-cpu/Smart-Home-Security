# Smart-Home-Security
Sistema antifurto IoT basato su ESP32 e MicroPython. Il progetto permette il monitoraggio e la gestione automatizzata della sicurezza domestica attraverso un'architettura ibrida (locale e remota), integrando sensori fisici, dashboard web e notifiche mobile.

## Demo
https://www.youtube.com/watch?v=zn8M-5acVwQ

## Funzionalità Principali
* **Gestione locale tramite tastierino:** L'utente può inserire il codice di sicurezza e selezionare la modalità di funzionamento direttamente dal tastierino numerico.
* **Modalità Giorno:** Prevede un tempo di uscita (20 secondi) per consentire l'allontanamento dell'utente. In caso di intrusione, un tempo di ingresso permette il disinserimento; l'allarme scatta dopo due tentativi di codice errati o mancati.
* **Modalità Notte:** Attiva i soli sensori perimetrali e chiude automaticamente la tenda. Non prevede tempi di ingresso, provocando un allarme immediato a ogni evento sospetto. Al disinserimento, la tenda viene riaperta.
* **Dashboard di monitoraggio:** Tutti i dati sono trasmessi via MQTT a Node-RED, che archivia gli eventi con timestamp per scopi statistici e fornisce un'interfaccia grafica divisa in "Security Hub" e "Log & Grafici".
* **Gestione remota via Telegram:** Integrazione di un bot Telegram per il controllo remoto del sistema e l'invio di notifiche push istantanee in caso di allarme o cambio di stato.


## Architettura del Sistema
Il software del sistema è sviluppato in MicroPython ed è strutturato in moduli per coordinare in modo efficiente l'infrastruttura IoT:

* Logica di Controllo e Stato: Il cuore del sistema è una classe principale (main) che coordina il funzionamento generale, gestendo la logica dell'antifurto, i cambi di stato e le interazioni tra tutti i componenti.
* Parametrizzazione: È presente una classe di configurazione (config) dedicata esclusivamente alla raccolta delle costanti e dei parametri di sistema (come le tempistiche e le impostazioni operative).
* Connettività e Avvio: La fase di inizializzazione è gestita dal file boot.py sull'ESP32, il quale si occupa di stabilire la connessione alla rete WiFi e di avviare la comunicazione MQTT.
* Comunicazione IoT: Lo scambio di messaggi avviene tramite il protocollo MQTT verso Node-RED (che gestisce l'interfaccia) e Telegram (per la gestione del bot e delle notifiche).

## Componenti Hardware
Il sistema utilizza una scheda ESP32 a cui sono collegati i seguenti dispositivi:
* Sensori:
  * Sensore di movimento PIR
  * Sensori magnetici
  * Accelerometro
* Attuatori e Output:
  * Buzzer
  * LED
  * Step-motor
  * Display OLED
* Dispositivi di Input:
  * Tastierino numerico

## Dashboard Node-RED
<p align="center">
  <img width="49%" alt="Security Hub" src="https://github.com/user-attachments/assets/bd758eae-cd89-4035-b21e-a67088f52b66" />
  <img width="49%" alt="Log & Grafici" src="https://github.com/user-attachments/assets/65607562-4b44-4299-ae24-57a0d4010312" />
</p>

## Bot Telegram
Scansiona il QR code qui sotto con il tuo smartphone per avviare il bot Telegram dedicato alla gestione dell'antifurto.
<p align="center">
  <img width="200" alt="QR Code Bot Telegram" src="https://github.com/user-attachments/assets/dde58dd8-fda8-457d-9f78-6b4ee349b6dc" />
</p>

## Team
Questo progetto è stato ideato, progettato e sviluppato da:
* **Dana Iannaccone** - [GitHub]()
* **Mara Mariano** - [GitHub](https://github.com/maraa-cpu)
* **Vincenzo Galdiero** - [GitHub]()


