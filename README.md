# Smart-Home-Security
Il sistema di antifurto è gestito tramite un tastierino numerico per l’inserimento del codice e la selezione della modalità. In modalità giorno, l’attivazione prevede un tempo di uscita per l’allontanamento dell’utente, al termine del quale si attivano tutti i sensori; in caso di intrusione, un tempo di ingresso consente il disinserimento, ma l'allarme scatta dopo due tentativi errati o mancati. In modalità notte, il sistema chiude automaticamente la tenda e attiva i soli sensori perimetrali senza alcun tempo di ingresso, provocando l'allarme immediato a ogni evento sospetto; al disinserimento, la tenda viene riaperta. Tutti i dati sono trasmessi via MQTT a Node-RED, che archivia gli eventi con timestamp per scopi statistici e fornisce una dashboard di monitoraggio. Il sistema supporta il controllo remoto e l’invio di notifiche istantanee tramite un bot Telegram.

## Demo
https://www.youtube.com/watch?v=zn8M-5acVwQ&t=3s

## Funzionalità Principali
* Gestione locale del sistema tramite tastierino numerico, che consente all'utente di inserire il codice e selezionare la modalità di funzionamento.
* Modalità Giorno con gestione dei ritardi: dopo l'inserimento del codice, il sistema avvia un tempo di uscita di 20 secondi per consentire l'allontanamento dell'utente prima dell'attivazione effettiva dell'antifurto e dei sensori.
* Interfaccia grafica completa per il controllo del sistema tramite dashboard, strutturata nelle sezioni principali "Security Hub" e "Log & Grafici".
* Trasmissione dei dati e avvisi da remoto tramite l'integrazione di un bot Telegram che invia notifiche push in tempo reale.


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


