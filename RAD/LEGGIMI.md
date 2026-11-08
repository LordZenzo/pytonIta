# PitStudio — ambiente di sviluppo per pytonIta

PitStudio è scritto in pytonIta (file `.pit`) e gira con l'interprete `pitonit`. Avvio: doppio clic su `PitStudio.cmd`
(oppure `..\pitonit\installazione\pitonit.exe rad.pit [cartella-progetto]`).

## Cosa contiene
| Parte | Cosa fa |
|---|---|
| **Editor** | colori per parole chiave italiane, funzioni predefinite, stringhe, commenti; numeri di riga; rientro automatico; chiusura di parentesi e virgolette; Trova/Sostituisci (Ctrl+F); commenta (Ctrl+/); duplica/sposta riga; segnalazione degli errori di sintassi mentre scrivi |
| **Suggerimenti** | dopo 2 lettere (o Ctrl+Spazio): parole chiave, funzioni predefinite, nomi del file, moduli dopo `importa`/`da`, membri dopo il punto (`tk.` → `Finestra`, `Percorso.` → `leggi_testo`…), frammenti (`se`, `per`, `definisci`, `classe`, `prova`, `finestra`… + Tab) |
| **Progetti** | cartella con `progetto.rad.json`; modelli *console*, *finestra*, *libreria*, *vuoto*; albero con nuovo file/cartella, rinomina, elimina, file principale ★; progetti recenti; sessione (schede aperte) ripristinata |
| **Risorse** | immagini (zoom), JSON (testo + albero con modifica e validazione), CSV/TSV (tabella), file binari (esadecimale); "Aggiungi risorse…" le copia in `risorse/` |
| **Progettista** | palette di 15 componenti, trascinamento e ridimensionamento con maniglie, griglia, selezione multipla, allinea/distribuisci, annulla/ripeti, ispettore delle proprietà, eventi → gestori; genera `nome.form.json`, `nome_ui.pit` (rigenerato) e `nome.pit` (la tua logica: PitStudio aggiunge solo i gestori mancanti) |
| **Programmi a mattonelle** | secondo modo di programmare, stile Scratch: *Nuovo programma a mattonelle* (barra 🧱, File o menu dell'albero). Ogni **funzione** ha la sua finestra di lavoro (anche staccabile in una finestra separata: clic destro sulla scheda) e il **flusso principale** ha la sua; le funzioni create compaiono come mattonelle nella categoria *Funzioni* (come istruzione e come valore). Forme e colori per i comandi: cappello giallo (inizio), blocchi arancioni a C (se, per ogni, ripeti, mentre, prova…), istruzioni (variabili rosse, scrivi/chiedi verdi, funzioni magenta), valori a pillola e condizioni a esagono (operatori azzurri, testo verde acqua, liste viola). Variabili: mattonelle *imposta*, *cambia*, *variabile* con elenco dei nomi e «Nuova variabile…» (locale o globale). **Collegamenti staccabili e spostabili**: afferra una mattonella e portala via (con le seguenti; Alt = solo lei, un valore esce dal suo ingresso), lasciala vicino a un punto di aggancio (evidenziato in giallo) per ricollegarla; sulla tavolozza = cestino. Annulla/ripeti, zoom, codice pytonIta generato in tempo reale con avvisi (ingressi vuoti, pile non collegate), Esegui. File: `nome.mattonelle.json` + `nome.pit` generato. **Conversione inversa**: clic destro su un `.pit` nell'albero (o File → «Converti il file corrente in mattonelle…», o lo strumento AI `converti_in_mattonelle`) lo trasforma in un programma a mattonelle `nome_mattonelle` senza toccare l'originale: le funzioni diventano finestre di lavoro, il codice libero diventa il flusso principale, `chiama`/`scrivi`/`imposta`/`se`/`per ogni`/… diventano mattonelle; classi e costanti restano come *codice di modulo* («⚙ Modulo»), le parti senza equivalente restano mattonelle di testo («codice», «espressione»); i commenti sopra le istruzioni sono conservati. Provato su un modulo vero di 677 righe (30 funzioni, 818 mattonelle): i suoi 28 test passano sul codice rigenerato |
| **Esecuzione** | F5 esegue il file principale con pitonit; console con colori, input per il programma, link dagli errori alla riga; Maiusc+F5 ferma |
| **Assistente AI** | chat con Claude che *usa l'ambiente*: legge e scrive file, modifica il codice, controlla la sintassi, esegue i programmi, apre file, disegna finestre nel progettista, esplora le librerie italiane. Conferme configurabili prima di scrivere/eseguire |
| **Impostazioni** | tutto è configurabile (Strumenti → Impostazioni): editor, tema (scuro/chiaro + colori personalizzati), esecuzione, AI, scorciatoie. Salvate in `~\.rad\config.json` |

## Novità della 1.12

- **Mattonelle: testo e codice in una finestra**. Codice, espressione, commento e testo si scrivono in una finestra media, ridimensionabile e che ricorda la misura; il codice può avere più righe (prima si apriva una sola riga).

## Novità della 1.11

- **Conversione di un intero progetto Python in pytonIta** (*File → Converti un progetto Python in pytonIta…*): crea una nuova cartella con tutti i `.py` tradotti in `.pit` (pacchetti compresi), copia gli altri file, verifica ogni traduzione e produce il rapporto `CONVERSIONE.md`. L'originale non viene toccato; i file non convertibili restano `.py`. Provata su un progetto reale con interfaccia grafica e test.
- `py2pit` ora funziona anche su un'installazione pulita (non dipende più dai percorsi di sviluppo).

## Novità della 1.10

- **Selezione vista dall'assistente**: il contesto indica le righe del codice selezionato e, se la selezione sparisce passando alla chat, ricorda l'ultima fatta; se non ce n'è, lo dice esplicitamente invece di lasciare l'assistente a indovinare.

## Novità della 1.9

- **Stima dei costi** dell'assistente a chiave API: in dollari, nello stato della chat e in *Statistiche dell'assistente* (totale, per richiesta, per modello); prezzi modificabili in `config.json` (`ai.prezzi`).

## Novità della 1.8

- Corretto: la disinstallazione toglieva dal desktop qualsiasi collegamento chiamato «PitStudio»; ora lo toglie solo se punta all'installazione che si sta rimuovendo.

## Novità della 1.7

- **Claude Code con l'abbonamento**: *Strumenti → Apri Claude Code nel progetto* (o il pulsante «⌨ Claude Code» nella chat) apre il Claude Code ufficiale nella cartella del progetto. PitStudio prepara `CLAUDE.md` e `.claude/settings.local.json` (hook locali: copia di sicurezza per «Annulla», controllo sintassi dopo ogni scrittura, registro). L'accesso lo fa l'utente nel programma di Anthropic; PitStudio non tocca credenziali. Vedi la guida, pagina «Claude Code con l'abbonamento».
- Corretto: due richieste dell'assistente nello stesso secondo potevano sovrascrivere il gruppo di modifiche.

## Novità della 1.6

- **Prima / dopo**: ogni modifica proposta dall'assistente si vede affiancata (righe tolte e aggiunte, con il «perché»).
- **Annulla le modifiche dell'assistente** (pulsante ↶ nella chat, cronologia delle ultime 50 richieste), senza git: copie in `.rad/storia`.
- **Limiti ai programmi** (memoria, processi) con i Job Object di Windows: 1024 MB / 20 processi per quelli dell'assistente.
- **Modello economico** (⚡ nella chat) e **compattazione** delle conversazioni lunghe.
- Interprete: `elimina(x)` attaccato alla parentesi è una chiamata, non `del (x)`.

## Novità della 1.5

- **Codice dell'assistente sempre controllato**: la sintassi dei `.pit`/`.py` si verifica prima di scrivere; gli errori tornano all'assistente (2 correzioni automatiche), poi decide l'utente.
- **Registro dell'assistente** (`.rad/ai_registro.jsonl`, locale) e *Strumenti → Statistiche dell'assistente*: token, codice valido al primo tentativo, esecuzioni.
- **Cache della conversazione**: a ogni passo si paga solo il nuovo (impostazione *Risparmia token*).

## Novità della 1.4

- **Pannello Librerie** (scheda a sinistra): elenco spuntabile con descrizione, per progetto.
- **Parole riservate come nomi** (`classe`, `con`, `da`, `prova`…) e **opzioni in italiano** (`chiave=`, `inverso=`, `codifica=`…): vedi `pitonit\NOMI.md`.
- **Scheda dei comandi** in una pagina nella guida; screenshot della guida aggiornati; finestra «Informazioni» con logo.
- L'**installatore** aggiorna una installazione esistente e chiede di chiudere PitStudio se è aperto.

## Imparare e correggere (v1.2)

- **Lezioni**: 16 lezioni con esercizi e soluzioni nella guida (gruppo «Imparare a programmare»); ogni esempio è verificato da `pitonit	ools\lezioni.py --verifica`.
- **Debugger**: punti di arresto (clic sul margine o F9), F6 per avviare, passo/entra/esci (F10/F11/Maiusc+F11), variabili, pila ed espressioni osservate. Funziona con `.pit` e `.py` (`rad\debug_runner.py`).
- **Errori con suggerimenti** 💡: la console e l'editor spiegano come correggere gli errori più comuni (`rad\diagnosi.pit`).

## Guida e Python classico

- **Guida integrata** (F1, Aiuto → Guida): 15 argomenti, ricerca, scheda per ogni parola chiave/funzione (F1 sulla parola nell'editor), esportabile in HTML (`aiuto\html\index.html`).
- **Python classico**: i file `.py` si aprono, colorano, controllano ed eseguono (F5) in inglese; clic destro → *Traduci in pytonIta* crea il `.pit`. Modello di progetto «Programma Python classico».

## Assistente AI: configurazione
1. Strumenti → Impostazioni → *Assistente AI* → inserisci la **chiave API Anthropic** (oppure imposta la variabile `ANTHROPIC_API_KEY`).
2. Scegli il modello (predefinito `claude-sonnet-5-5`), i limiti e se vuoi le conferme.
3. Apri un progetto e scrivi nella chat. *Invio* invia, *Maiusc+Invio* va a capo.
La chiave resta solo nel tuo `config.json`; la conversazione di ogni progetto è in `<progetto>\.rad\chat.json`.
Strumenti a disposizione dell'AI: `stato_ide`, `elenca_file`, `leggi_file`, `scrivi_file`, `modifica_file`, `cerca_nel_progetto`,
`controlla_sintassi`, `esegui_programma`, `apri_file`, `elimina_file`, `ottieni_form`, `imposta_form`, `tipi_mattonelle`, `ottieni_mattonelle`, `imposta_mattonelle`, `membri_modulo`.
Il suo "manuale" del linguaggio è `rad\manuale.md` (lo puoi leggere da Strumenti → Manuale pytonIta).

## Scorciatoie (modificabili)
Ctrl+S salva · Ctrl+Maiusc+S salva tutto · Ctrl+O apri progetto · Ctrl+N nuovo file · F5 esegui · Maiusc+F5 ferma ·
Ctrl+F trova · Ctrl+G vai a riga · Ctrl+/ commenta · Ctrl+Spazio suggerimenti · Ctrl+J chat · Ctrl+W chiudi scheda ·
Ctrl++/− dimensione del testo · Alt+↑/↓ sposta riga · Ctrl+D duplica.

## Progettista: come si usa
1. *Nuova finestra* (barra o clic destro nell'albero). 2. Scegli un componente e clicca sulla finestra (o doppio clic nella palette).
3. Trascina, ridimensiona, modifica le proprietà a destra. Nel campo *Evento* premi ⏎ per creare il gestore e saltare al codice.
4. **Salva** genera i file; **Prova** esegue la finestra. Doppio clic su un componente apre il suo gestore.

## Struttura del codice (`rad\`)
`config` impostazioni · `tema` colori · `parole` suggerimenti · `editor` · `progetto` (modello + pannello) · `risorse` (visualizzatori) ·
`esecuzione` (processi + console) · `form_modello` (finestre e generazione del codice, senza grafica) · `progettista` · `ai` (client + strumenti + agente) ·
`mattonelle_modello` (programma a mattonelle, collegamenti, funzioni, generatore di codice) · `mattonelle_disegno` (forme, colori, aggancio) · `mattonelle_ui` (area di lavoro, tavolozza, editor) · `mattonelle_converti` (da .pit a mattonelle) · `chat` · `ponte_ui` (thread → interfaccia) · `dialoghi` · `impostazioni` · `finestra` (assemblaggio).

## Prove
`..\pitonit\installazione\pitonit.exe tests\prova_xxx.pit` — `prova_parole`, `prova_editor`, `prova_form`, `prova_progetto`,
`prova_esecuzione`, `prova_risorse`, `prova_progettista`, `prova_mattonelle` (modello e codice), `prova_disegno`, `prova_mattonelle_ui` (trascinamento simulato), `prova_converti`, `prova_converti_reale`, `prova_converti_app`, `prova_mattonelle_app`, `prova_app` (avvio completo, esecuzione, AI con un server API simulato).
`tests\schermata.pit [scuro|chiaro]` salva schermate in `docs\`.
