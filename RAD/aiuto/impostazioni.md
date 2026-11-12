# Impostazioni

Apri *Strumenti → Impostazioni…* (o l'icona dell'ingranaggio). **Applica** applica subito senza chiudere, **OK** applica e chiude. Tutto viene salvato in `C:\Users\<tu>\.rad\config.json`:
per riportare PitStudio ai valori iniziali basta cancellare quel file.

![La finestra delle impostazioni](immagini/impostazioni.png)

## Tema

| Opzione | Descrizione |
|---|---|
| Tema | **scuro** o **chiaro** (si cambia anche da *Visualizza → Tema chiaro / scuro*) |
| Colori personalizzati | per ogni tema puoi cambiare sfondo, pannelli, editor, selezione, accento, i colori della sintassi (parole chiave, funzioni, stringhe, commenti, numeri…) e quello degli errori. Clic sul quadratino per scegliere il colore; vuoto = quello del tema |

## Editor

| Opzione | Descrizione |
|---|---|
| Carattere e dimensione | carattere a larghezza fissa (predefinito Consolas 11); anche con **Ctrl +/−** |
| Spazi per tabulazione | 4 per default |
| Numeri di riga, riga corrente evidenziata, a capo automatico | attivabili a piacere |
| Chiudi automaticamente parentesi e virgolette | per scrivere più in fretta |
| Suggerimenti automatici e ritardo | puoi spegnerli (restano su **Ctrl+Spazio**) o regolarne la prontezza |
| Salvataggio automatico | dopo N secondi dall'ultima modifica (0 = mai) |
| Variabili omonime | evidenzia le variabili con lo stesso nome usato per cose diverse |
| Guida verticale | disegna una linea sottile alla colonna scelta (0 = nessuna; per esempio 100) |
| Errori gravi | sottolinea in rosso gli errori che impedirebbero al programma di partire (vedi «I trabocchetti più comuni») |
| Copia di sicurezza | copia periodica dei file non salvati, da ripristinare dopo una chiusura improvvisa (e ogni quanti secondi) |

## Esecuzione

| Opzione | Descrizione |
|---|---|
| Interprete pitonit | vuoto = quello di PitStudio |
| Argomenti del programma | validi per ogni esecuzione |
| Salva tutto prima di eseguire | consigliato |
| Pulisci la console a ogni esecuzione | per vedere solo l'ultima prova |

## Assistente AI

| Opzione | Descrizione |
|---|---|
| Chiave API Anthropic | obbligatoria per usare l'assistente |
| Modello | quale modello usare; l'elenco nel menu della chat si modifica in `config.json` (`ai.modelli`) |
| Lunghezza massima della risposta | token massimi per risposta |
| Passi massimi per richiesta | quanti strumenti può usare l'assistente di seguito prima di fermarsi |
| Conferme su scrittura ed esecuzione | consigliate; spegnile solo se ti fidi del lavoro automatico |
| Includi file attivo e selezione | manda all'assistente il contesto dell'editor |
| Risparmia token riusando la conversazione | attiva la cache dell'API: la conversazione già letta costa molto meno a ogni passo (consigliato) |
| Correzioni automatiche del codice | quante volte l'assistente corregge da solo un errore di sintassi prima di chiedere a te (0 = mai) |
| Modello economico | usato dalla casella «⚡ economico» e da «Spiega» (per risparmiare) |
| Accorcia la conversazione oltre questi token | quando la chat diventa lunga i vecchi risultati vengono accorciati (0 = mai) |
| Limiti dei programmi dell'assistente | memoria (MB) e numero di processi che i programmi eseguiti dall'assistente possono usare (0 = nessun limite) |
| Prezzi (solo in `config.json`, `ai.prezzi`) | per la stima dei costi: `{"modello": [ingresso, uscita, cache_lettura, cache_scrittura]}` in dollari per milione di token. Sono già inclusi Sonnet 5.5, Haiku 5.5 e Opus 5.5 ai prezzi pubblicati; aggiungi o correggi qui gli altri |
| Registro | salva in locale token e validità del codice generato (`.rad\ai_registro.jsonl` nel progetto) |
| Indirizzo dell'API | per usare un servizio compatibile diverso |
| Istruzioni aggiuntive | testo che l'assistente legge a ogni richiesta (stile, convenzioni del tuo progetto…) |

## Scorciatoie

Ogni scorciatoia si scrive nel formato di Tk: `Control-s`, `Control-Shift-S`, `F5`, `Alt-Up`… Le modifiche valgono subito. L'elenco completo è in [Scorciatoie da tastiera](#scorciatoie).

## Disposizione

La dimensione della finestra, dei pannelli e quali pannelli sono visibili si salvano da soli quando chiudi PitStudio.
