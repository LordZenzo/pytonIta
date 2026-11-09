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

## Novità della 1.26

- **Progettista più completo**: **barra dei menu** (voci collegate ai gestori, separatori, apertura di altre finestre), **timer**, **Schede** e **Riquadri con componenti dentro**, **ancoraggio ai bordi** (i componenti si allargano o restano attaccati quando si ridimensiona la finestra), **pulsanti che aprono altre finestre** (anche come dialogo) e **ordine di tabulazione**. Il codice generato funziona anche dopo l'esportazione in Python.

## Novità della 1.25

- **Maschere collegate ai dati**: dalla scheda di un database, **▤ Maschera…** (o *Database → Crea una maschera dalla tabella…*) crea nel progetto una finestra del progettista già collegata alla tabella: ricerca, elenco dei record, campi, **Nuovo / Salva / Elimina / Annulla** con controlli (campi obbligatori, numeri). Funziona con SQLite e MySQL (la password è chiesta all'avvio, mai salvata), si modifica nel progettista e si esporta in Python. Il collegamento sta in `fonte_dati.pit` (`FonteDati`, `MascheraDati`), usabile anche con finestre disegnate a mano.

## Novità della 1.24

- **MySQL provato su un server vero** (MySQL 9.1 di WAMP): collegamento, tabelle, viste, chiavi esterne, modifica dei dati, CSV, SQL a più comandi, creazione guidata di tabelle e installazione del driver `pymysql` dal programma. Corretto un errore che impediva i comandi SQL con il segno `%` (per esempio `LIKE 'P%'`) su MySQL. Nuovo test `prova_database_mysql.pit` (si attiva con `RAD_PROVA_MYSQL=1`).

## Novità della 1.23

- **Crea l'eseguibile (.exe)** (*File → Crea l'eseguibile (.exe)…*): converte il progetto in Python e lo impacchetta con PyInstaller in un ambiente separato dentro `.rad/build`, mostrando l'avanzamento. Opzioni: nome, icona, un solo file o cartella, con o senza finestra nera. Il risultato è in `dist`; chi lo riceve non ha bisogno di Python. Serve Python 3 sul computer di chi costruisce e internet la prima volta. Immagini, `.json`, database e altri file del progetto sono inclusi.

## Novità della 1.22

- **Gestore di database** (menu *Database*): SQLite come predefinito (un file `.db` nel progetto, apribile anche con doppio clic) e MySQL/MariaDB come alternativa (driver `pymysql`, installabile dal programma; la password non viene salvata). Una scheda per database con l'elenco di tabelle e viste, **dati modificabili** (doppio clic sulla cella, filtro SQL, ordinamento, pagine, nuova riga, elimina righe), **struttura** delle tabelle, **creazione guidata di tabelle e colonne** con l'istruzione SQL in anteprima, **importazione ed esportazione CSV** e un **editor SQL** con più comandi, risultati in tabella, storia e suggerimenti.

## Novità della 1.21

- **Esporta il progetto come Python** (*File → Esporta il progetto come Python…*): crea una cartella di `.py` che gira con un Python normale, senza pytonIta. Dentro ci sono anche `requirements.txt` con le librerie scientifiche usate (e le versioni provate), gli script `installa_librerie.bat` / `.sh` e un `LEGGIMI.txt` per chi riceve il programma. Il convertitore (`pitonit/tools/pit2py.py`) traduce parole chiave, funzioni predefinite, moduli italiani e i loro nomi, metodi e opzioni; non tocca i nomi scelti dall'utente. Verificato: le parole chiave coincidono con quelle lette da `pitonit` su tutto il codice del progetto e su 152 moduli della libreria standard (andata e ritorno).

## Novità della 1.20

- **Campi numerici con freccette** nell'ispettore del progettista (su/giù, rotella, tasti freccia), con i limiti naturali di ogni valore: un componente resta dentro la finestra, il cursore tra il suo minimo e massimo, la barra tra 0 e il suo massimo.
- **Albero: gestione delle colonne**: finestra «Modifica…» con nome, larghezza in pixel e allineamento di ogni colonna, aggiunta, rimozione, ordine. Anteprima e codice generato le rispettano.
- **La finestra si ridimensiona trascinando** le maniglie fuori dal bordo destro, da quello inferiore e dall'angolo.
- **Suggerimenti vicino al mouse anche con più monitor** (prima finivano su un altro schermo).
- **Pannello Librerie**: le librerie già importate dal file aperto risultano spuntate; spuntarne una aggiunge `importa …` al codice, togliendo la spunta la riga sparisce.
- **Programmi a mattonelle con una finestra**: nuovo modello di progetto «Mattonelle a finestra» con un esempio pronto (etichetta, campo, pulsante) e la nuova categoria di mattonelle **Finestre** (16 mattonelle).
- **Modello «Libreria» spiegato**: pacchetto completo con funzione, classe, prova e `LEGGIMI.md` che spiega come funziona e come si riusa.
- **Barra degli strumenti personalizzabile**: *Visualizza → Personalizza la barra degli strumenti…* (o clic destro sulla barra) permette di mettere e togliere come pulsanti **qualsiasi comando dei menu**, riordinarli, aggiungere separatori e uno spazio che porta i pulsanti a destra; c'è «Predefinita» per tornare all'inizio. La scelta si salva.
- **Suggerimento su ogni pulsante** dell'interfaccia principale (barra, linguette dei pannelli, X delle schede, barra di stato, mattonelle, schermata di benvenuto).
- Il pulsante **Debug** della barra ora avvia il debug **passo passo** dalla prima riga (il menu Esegui resta com'era).
- **Rotella del mouse** nei campi numerici dell'ispettore.
- **Pannello Librerie**: se una libreria resta spuntata perché il file aperto la importa in una forma che non cancello da solo (per esempio `da interfaccia importa …`), il pannello lo spiega e indica le righe.
- Nella scelta del modello di nuovo progetto si vedono i nomi **«Mattonelle a console»** e **«Mattonelle a finestra»** al posto degli identificativi interni.

## Novità della 1.19

- **Ridimensionamento con le maniglie nel progettista**: con il mouse vero la maniglia afferrata veniva distrutta e ricreata a ogni movimento, e Windows smetteva di mandarle i movimenti: la dimensione cambiava di un solo passo e poi si fermava. Ora contorno e maniglie vengono solo spostati. Provato anche con il mouse reale (`tests/prova_maniglie.pit`).

## Novità della 1.18

- **Anteprima del progettista fedele alla finestra vera**: prima i componenti ereditavano i colori scuri di PitStudio (pulsanti piatti, campi scuri, barra di avanzamento blu) e si discostavano molto dal programma in esecuzione. Ora l'anteprima ha l'aspetto predefinito di Windows, uguale alla finestra generata. Misurato confrontando le schermate: i pixel diversi sono scesi dal 58,8 % allo 0,3 % (restano piccole differenze nelle frecce della casella combinata, nella barra di avanzamento e nelle intestazioni dell'albero, che nel programma vero usano il tema nativo di Windows). Test: `tests/prova_anteprima.pit`.
- **Caselle e opzioni**: nella finestra vera ora sono allineate a sinistra come nell'anteprima (prima erano centrate). Le caselle già spuntate all'avvio restano spuntate anche se nessuno conserva l'oggetto della finestra (errore dell'avvio generato).
- Il bordo della finestra in anteprima non sposta più i componenti di un pixel.

## Novità della 1.17

- **Suggerimenti (tooltip) su tutti i pulsanti**: oltre alla barra principale, ora li hanno anche la barra delle mattonelle, il progettista (compresi «Griglia» e «Allinea»), la console, il debug (con i tasti rapidi), la ricerca nell'editor, l'albero del progetto, le barre di immagini e JSON e la chat con l'assistente. Il fumetto compare dopo mezzo secondo e resta sempre dentro lo schermo. Per i programmatori: `rad.stile.suggerisci(widget, testo)`.

## Novità della 1.16

- **Quasi tutto il linguaggio a mattonelle**: frasi (f-string), `con … come …`, `solleva`, generatori (`produci`), `elimina`, `cambia … op= …`, dizionari con coppie, insiemi, `*args`/`**kwargs`, operatori `| & ^ << >>`, `per … altrimenti`, `mentre … altrimenti`, `da … importa …`, comprensioni di dizionario, tuple/liste fino a 12 elementi. Gli ingressi facoltativi vuoti non occupano più spazio.
- **Prova di fedeltà**: le ~1.700 funzioni e metodi di PitStudio stesso, convertiti in mattonelle e rigenerati, hanno lo **stesso albero sintattico** degli originali (`tests/prova_mattonelle_fedelta.pit`); restano come testo circa lo 0,25 % delle istruzioni.
- **Interprete**: `per w, in x:` (virgola finale prima di `in`) ora è accettato. `py2pit` traduce anche i `case (` con il pattern tra parentesi su più righe (249 moduli della libreria standard tradotti con struttura identica).

## Novità della 1.15

- **Programmi a oggetti interamente a mattonelle**: classi con una pagina per metodo (＋ Classe, ＋ Metodo), categoria *Oggetti* (attributi, imposta su attributi/tuple, chiamata di metodi, opzioni `nome=valore`, tupla, lambda), comprensioni, `a se c altrimenti b`, catene di confronti, `è`, fette, dizionari, `eccetto Tipo come nome`.
- **La conversione in mattonelle ora porta con sé le classi**: su un programma reale con interfaccia grafica (modfile_gui, 1.100 righe) restano come testo meno dell'1% delle istruzioni; il programma rigenerato dalle mattonelle supera gli stessi test e la stessa prova dell'interfaccia.

## Novità della 1.14

- **Mattonelle**: il testo su più righe o molto lungo (codice, espressione…) non esce più dalla mattonella: si vede su una riga con «⏎» al posto degli a capo e «…» se è lungo; il testo completo si legge e si modifica nella finestra.

## Novità della 1.13

- **Finestra del testo nelle mattonelle**: casella «A capo automatico» per andare a capo o no (per il codice parte spento, per i testi acceso; la scelta è ricordata).

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
