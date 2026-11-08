# Primi passi

Questa guida ti porta dal primo avvio a un programma che funziona. Ci vogliono circa dieci minuti.

## 1. Crea un progetto

Dalla schermata di benvenuto scegli **Nuovo progetto** (oppure il pulsante **+** nella barra, o *File → Nuovo progetto…*).
Dai un nome (per esempio `Saluti`), lascia la cartella proposta e scegli il modello **Programma da console**. Premi **Crea progetto**.

PitStudio crea la cartella, il file `principale.pit` e lo apre nell'editor.

## 2. Leggi e modifica il programma

Il programma di esempio chiede il nome e conta fino a tre:

```pit
definisci principale():
    nome = leggi("Come ti chiami? ")
    stampa(f"Ciao, {nome}!")
    per i in intervallo(1, 4):
        stampa("Conto:", i)


se __nome__ == "__main__":
    principale()
```

Prova a scrivere una nuova riga dopo il ciclo: digita `sta` e compare l'elenco dei suggerimenti. Premi **Tab** (o Invio) per accettare `stampa`.

## 3. Eseguilo

Premi **F5** o il pulsante blu **Esegui**. In basso si apre la console: scrivi il tuo nome nella riga in fondo e premi Invio.
Se c'è un errore, la console lo mostra in italiano con un link alla riga: un clic e l'editor ti ci porta.

## 4. Disegna una finestra

Clic destro nella cartella del progetto (nell'albero a sinistra) → **Nuova finestra (progettista)…**, nome `Saluto`.
Si apre il [progettista](#progettista): scegli *Pulsante* nella palette, clicca sulla finestra, scrivi il testo nella proprietà **Testo**.
Nel campo **Evento: clic** premi ⏎: PitStudio crea il gestore nel codice e ci porta lì. Scrivi `stampa("Cliccato!")`, poi premi **Prova** nella barra del progettista.

## 5. Prova le mattonelle

Premi il pulsante **▦** nella barra (*Nuovo programma a mattonelle*). Dalla tavolozza a sinistra trascina **scrivi** sotto «Quando parte il programma»
e premi **Esegui**. Guarda a destra il codice che PitStudio ha generato (pulsante **Codice**). Vedi [Programmi a mattonelle](#mattonelle).

## 6. Chiedi all'assistente

Apri *Strumenti → Impostazioni → Assistente AI* e inserisci la tua chiave API. Poi apri la chat (**Ctrl+J**) e scrivi per esempio:
*«Aggiungi al programma un contatore che chiede quante volte salutare»*. Vedi [Assistente AI](#assistente).

> **Nota:** tutto ciò che fai viene salvato in file normali nella cartella del progetto: puoi aprirli, copiarli o versionarli come vuoi.
