# Smart-Home-Security
Il sistema di antifurto è gestito tramite un tastierino numerico per l’inserimento del codice e la selezione della modalità. In modalità giorno, l’attivazione prevede un tempo di uscita per l’allontanamento dell’utente, al termine del quale si attivano tutti i sensori; in caso di intrusione, un tempo di ingresso consente il disinserimento, ma l'allarme scatta dopo due tentativi errati o mancati. In modalità notte, il sistema chiude automaticamente la tenda e attiva i soli sensori perimetrali senza alcun tempo di ingresso, provocando l'allarme immediato a ogni evento sospetto; al disinserimento, la tenda viene riaperta. Tutti i dati sono trasmessi via MQTT a Node-RED, che archivia gli eventi con timestamp per scopi statistici e fornisce una dashboard di monitoraggio. Il sistema supporta il controllo remoto e l’invio di notifiche istantanee tramite un bot Telegram.

## Demo
https://www.youtube.com/watch?v=zn8M-5acVwQ&t=3s

## Dashboard Node-RED
![Security Hub]<img width="1439" height="789" alt="Screenshot 2026-01-28 alle 20 02 16" src="https://github.com/user-attachments/assets/bd758eae-cd89-4035-b21e-a67088f52b66" />

![Log & Grafici]<img width="1435" height="810" alt="Screenshot 2026-01-28 alle 20 06 00" src="https://github.com/user-attachments/assets/65607562-4b44-4299-ae24-57a0d4010312" />
