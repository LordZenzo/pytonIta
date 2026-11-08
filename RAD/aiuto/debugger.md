# Il debugger

Il debugger esegue il programma sotto il tuo controllo: lo **fermi** dove vuoi, **guardi** le variabili e **avanzi** una riga alla volta. È lo strumento giusto quando il programma parte ma fa qualcosa di sbagliato. Una spiegazione con un esempio è nella [lezione 12](#lezione-12).

![Il pannello Debug](immagini/debugger.png)

## Punti di arresto

- **Clic sul margine** a sinistra del numero di riga, oppure **F9** con il cursore sulla riga: compare un pallino rosso. Un altro clic lo toglie.
- *Esegui → Togli tutti i punti di arresto* li cancella tutti.
- I punti di arresto sono salvati con il progetto e restano alla prossima apertura.

## Avviare

| Comando | Cosa fa |
|---|---|
| **F6** o il pulsante 🐞 | esegue il file principale (o il file aperto) e si ferma sui punti di arresto |
| *Esegui → Debug: avvia passo passo dalla prima riga* | si ferma subito alla prima riga |

Mentre il debugger è in funzione, il programma è un processo normale: puoi rispondere a `leggi()` nella console.

## Il pannello Debug

Appare sotto l'editor quando parte il debugger.

| Zona | Cosa mostra |
|---|---|
| **Barra dei comandi** | Continua, Passo, Entra, Esci, Ferma |
| **Variabili** | le variabili visibili nel punto in cui il programma è fermo: nome, valore, tipo |
| **Pila delle chiamate** | l'elenco delle funzioni attive; un clic su una riga mostra quel punto nell'editor |
| **Espressioni osservate** | scrivi un'espressione (per esempio `totale / lunghezza(voti)`) e premi Invio: il suo valore si aggiorna a ogni sosta. Per toglierla: seleziona e premi Canc |

La riga in cui il programma è fermo è evidenziata di giallo e segnata con ▶ nel margine.

## I comandi

| Comando | Tasto | Cosa fa |
|---|---|---|
| ▶ Continua | **F5** | prosegue fino al prossimo punto di arresto o alla fine |
| ⤼ Passo | **F10** | esegue una riga (una chiamata di funzione conta come una riga sola) |
| ↧ Entra | **F11** | entra nella funzione chiamata dalla riga corrente |
| ↥ Esci | **Maiusc+F11** | termina la funzione corrente e torna a chi la chiamava |
| ■ Ferma | **Maiusc+F5** | interrompe il programma |

## Cosa vedi e cosa no

- Il debugger si ferma solo nel **tuo codice** (i file `.pit` e `.py` del progetto), non dentro le librerie.
- Funziona con i programmi `.pit` e `.py`. I programmi a mattonelle si debuggano nel `.pit` che generano.
- Nei programmi con una **finestra** (interfaccia grafica) il debugger si ferma sui punti di arresto delle funzioni chiamate dai pulsanti; mentre è fermo la finestra non risponde.
