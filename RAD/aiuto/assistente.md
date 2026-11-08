# L'assistente AI

L'assistente è **Claude** e lavora dentro PitStudio: non solo ti risponde, ma può **usare l'ambiente** al posto tuo, sul progetto aperto.

![La chat con l'assistente](immagini/assistente.png)

## Configurazione (una volta sola)

1. Apri *Strumenti → Impostazioni → Assistente AI*.
2. Incolla la tua **chiave API Anthropic** (la chiave resta nel tuo computer, nel file `~\.rad\config.json`). In alternativa imposta la variabile d'ambiente `ANTHROPIC_API_KEY`.
3. Scegli il **modello** (anche dal menu in alto nella chat) e le **conferme** (vedi sotto). Premi OK.

La barra di stato in basso mostra «● Assistente AI pronto» quando la chiave c'è.

## Usare la chat

Apri la chat con **Ctrl+J** (o il pulsante *Assistente*). Scrivi la richiesta e premi **Invio** (**Maiusc+Invio** va a capo). L'assistente risponde nella cronologia;
quando usa l'ambiente lo vedi in riga: 🛠 nome dello strumento, ✔ o ✖ con l'esito.

- Con **Includi file attivo e selezione** (predefinito) l'assistente sa quale file hai aperto, a che riga sei e cosa hai selezionato.
- I blocchi di codice nelle risposte hanno i pulsanti **Copia**, **Inserisci nell'editor** e **Nuovo file**.
- **■ Ferma** interrompe il lavoro in corso; **Nuova chat** ricomincia da zero. La conversazione di ogni progetto è salvata in `<progetto>\.rad\chat.json`.

## Cosa può fare

| Strumento | Cosa fa |
|---|---|
| `stato_ide` | vede progetto, schede aperte, file attivo, selezione e le ultime righe della console |
| `elenca_file`, `leggi_file`, `cerca_nel_progetto` | esplora il progetto (legge anche le modifiche non ancora salvate) |
| `scrivi_file`, `modifica_file` | crea o modifica file (sostituzioni precise) |
| `controlla_sintassi` | verifica il codice in italiano |
| `esegui_programma` | esegue un file e legge output ed errori |
| `apri_file`, `elimina_file` | apre un file nell'editor; elimina (chiede sempre conferma) |
| `ottieni_form`, `imposta_form` | legge e **disegna finestre** nel progettista |
| `tipi_mattonelle`, `ottieni_mattonelle`, `imposta_mattonelle` | costruisce **programmi a mattonelle** |
| `converti_in_mattonelle` | converte un `.pit` in mattonelle |
| `membri_modulo` | scopre i nomi delle librerie in italiano |

## Esempi di richieste

- *«Spiegami questo codice»* (con del codice selezionato).
- *«Trova perché l'ultima esecuzione dà errore e correggilo»*, oppure *Strumenti → Chiedi all'AI di correggere l'ultimo errore*.
- *«Crea una finestra con un campo di testo, un pulsante "Calcola" e un'etichetta per il risultato; il pulsante deve raddoppiare il numero»*.
- *«Aggiungi il salvataggio dei dati in un file JSON»*.
- *«Costruisci a mattonelle un programma che stampa la tabellina del 7»*.
- *«Converti `vecchio.pit` in mattonelle e dimmi cosa è rimasto come testo»*.

## Codice sempre controllato

Prima di scrivere un file `.pit` o `.py`, PitStudio ne controlla la **sintassi**. Se il codice dell'assistente ha un errore, **tu non lo vedi nemmeno**: l'errore torna all'assistente, che corregge e riprova (fino a 2 correzioni automatiche). Se non ci riesce, ti chiede se salvare comunque il file per correggerlo a mano. Il file non viene toccato finché il codice non è valido o non lo decidi tu.

## Quanto costa

L'assistente usa la tua chiave API e i costi dipendono dal modello e dal testo scambiato. Per tenerli bassi:

- la **conversazione già letta viene riusata** (cache dell'API): a ogni passo si paga solo ciò che è nuovo;
- l'assistente legge solo le parti di file che servono e modifica poche righe invece di riscrivere tutto;
- in basso nella chat vedi i token della conversazione, con quanti letti dalla cache;
- con *Strumenti → Statistiche dell'assistente* vedi, per il progetto: richieste, token, quanti file erano **validi al primo tentativo**, quanti corretti da solo, quanti programmi eseguiti con successo. I dati restano sul tuo computer (`.rad\ai_registro.jsonl`) e si disattivano nelle impostazioni.

Per i lavori semplici (spiegare un errore, una piccola correzione) puoi scegliere dal menu della chat un modello più economico.

## Sicurezza e privacy

- **Conferme**: per default l'assistente chiede il permesso prima di **scrivere file** e prima di **eseguire programmi**; vedi un'anteprima di cosa farà. Eliminare un file chiede sempre conferma. Le conferme si regolano nelle impostazioni.
- L'assistente lavora **solo dentro la cartella del progetto**: non può leggere né scrivere fuori.
- Il contenuto che gli mostri (file letti, output dei programmi, ciò che scrivi) viene inviato ad Anthropic per ottenere la risposta, come in qualsiasi uso dell'API. Non aprire progetti con dati riservati se non vuoi che vengano inviati.
- Puoi aggiungere **istruzioni permanenti** (per esempio «rispondi in modo molto breve») nelle impostazioni.

> **Nota:** i costi dell'API dipendono dal modello e da quanto testo viene scambiato; in basso nella chat vedi i token usati in questa conversazione.
