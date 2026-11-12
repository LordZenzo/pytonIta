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

## Novità della 2.10

- **Dove prendere la chiave API**: nelle impostazioni dell'assistente, accanto a ogni chiave (Claude, Gemini, DeepSeek, OpenAI, OpenRouter) c'è il collegamento alla pagina della piattaforma dove crearla; per Ollama il collegamento al download e ai modelli.

## Novità della 2.9

- **La memoria nel debugger**: il pulsante «🧠 Memoria» mostra i nomi e gli oggetti come scatole con le frecce; quando due nomi sono lo stesso oggetto lo si vede subito (frecce arancioni nella stessa scatola). Pensato per chi impara: l'alias di una lista è l'errore più comune.

## Novità della 2.8

- **Modalità insegnante**: *Esercizi → Classe →* **Crea un pacchetto con i miei esercizi…** (un file `.pitesercizi` da dare agli allievi) e **Importa un pacchetto di esercizi…**; i file dei progressi comprendono anche i quiz delle lezioni e il report della classe mostra le lezioni superate da ogni allievo.

## Novità della 2.7

- **Server MCP**: gli strumenti di PitStudio (leggere e scrivere file con il controllo di sintassi e degli errori gravi, ottenere e impostare le finestre, cercare, esplorare i moduli) per altri agenti — Claude Code, Cursor… — senza che PitStudio sia aperto. *Strumenti → Collega altri agenti (MCP)…* mostra i comandi da copiare. Non cancella file e non esegue programmi (salvo `--consenti-esecuzione`). Provato con un cliente finto e con il processo vero su stdin/stdout, non con Claude Code o Cursor.

## Novità della 2.6

- **Professore a indizi**: il pulsante «💡 Indizio» nella chat del professore chiede un aiuto alla volta, sempre più preciso (da 1 a 4); la soluzione intera solo se l'allievo si arrende.
- **L'assistente vede la finestra**: strumento `vedi_anteprima` (schermata del form nel progettista) per Claude, OpenAI e OpenRouter (Ollama solo con un modello «vision» e `ai.immagini_ollama`); le immagini vecchie si tolgono dalla conversazione.

## Novità della 2.5

- **Altri fornitori per l'assistente AI**: OpenAI, OpenRouter (una chiave per molti modelli) e **modelli sul tuo computer con Ollama** (nessuna chiave, nessun costo, i dati non escono dal PC; PitStudio legge da Ollama l'elenco dei modelli scaricati). Si scelgono in Impostazioni → Assistente AI. Provati con server finti: non con i servizi veri.

## Novità della 2.4

- **Disposizione in riga e in colonna** (finestra, Riquadro, pagina di Schede): i componenti uno dopo l'altro, con «Si allarga» per chi deve prendere lo spazio che avanza. Si riordinano trascinando, con le frecce o dall'ispettore. Il programma usa lo stesso calcolo della griglia, quindi quello che vedi è quello che ottieni.

## Novità della 2.3

- **PostgreSQL**: *Database → Collegati a PostgreSQL…* (driver `psycopg2`, installabile dal menu), tabelle e viste dello schema `public`, creazione e modifica di tabelle e colonne, e il tipo di database `postgres` nelle fonti dati dei programmi (la password si chiede all'avvio e non si salva). Provato con un driver finto: non c'è stato modo di provarlo con un server vero.
- **Trigger e testi tra dollari nel pannello SQL**: `CREATE TRIGGER … BEGIN …; …; END;` e `$$ … $$` non si spezzano più sui «;».

## Novità della 2.2

- **Area scorrevole**: un Riquadro con «Scorrevole» a sì mostra nel programma solo la parte «visibile» e si scorre con le barre o la rotella. Nel progettista si disegna grande quanto tutto il contenuto. Pagina «Area scorrevole» nella guida del progettista; `scorrevole.pit` viene copiato nel progetto.
- **Guida verticale nell'editor**: Impostazioni → Editor → «Guida verticale alla colonna» (0 = nessuna).

## Novità della 2.1

- **Nomi di una lettera**: `l` e `I` non si possono usare come nomi (si confondono con il numero 1: errore grave). Le altre lettere sole ricevono un avviso arancione nell'editor, tranne `i`, `j`, `k`, `n`, `x`, `y`, `z`.

## Novità della 2.0 (controllo prima dell'esecuzione e nuovi nomi)

> **Attenzione: la 2.0 non è compatibile con i programmi scritti con la 1.x.** Cambiano i nomi delle funzioni predefinite (`testo`→`tipo_testo`, `lunghezza`→`lunghezza_di`, `leggi`→`leggi_tastiera`, `genitore`→`classe_base`…), `e` e `o` non sono più ammessi come nomi di variabile e il controllo blocca i programmi con errori gravi. L'elenco completo dei nomi è in `pitonit/NOMI.md`.

- L'interprete controlla ogni programma `.pit` (e ogni modulo `.pit` importato) **prima di eseguirlo** e lo blocca se trova un errore grave: una parola chiave usata come nome (`pass`, `classe = ...`, `definisci f(da, a)`) oppure una funzione predefinita nascosta da una variabile e poi richiamata (`testo = "a"` ... `testo(5)`).
- `pitonit -m _controlla programma.pit` mostra anche gli avvisi (nomi inglesi come `print`, nomi non definiti). `# controlla: ok` salta una riga, `# controlla: ignora-file` un file, `PITONIT_SENZA_CONTROLLO=1` il controllo.
- Anche `e` e `o` non si possono usare come nomi di variabile (sono gli operatori «and» e «or»): al loro posto `evento`, `errore`, `elemento`… Tutto il codice, gli esempi e le lezioni di PitStudio sono stati aggiornati.
- **Nuovi nomi delle funzioni predefinite.** I nomi italiani più comuni, che chiunque darebbe a una variabile, ora hanno un trattino basso e non si confondono più: `tipo_testo`, `tipo_lista`, `tipo_intero`, `tipo_decimale`, `tipo_dizionario`, `tipo_insieme`, `tipo_tupla`, `lunghezza_di`, `somma_di`, `massimo_di`, `minimo_di`, `intervallo_di`, `tipo_di`, `leggi_tastiera`, `classe_base` (era `genitore`), `valore_assoluto`, `ordinato_di`, `inverso_di`, `mappa_funzione`, `tutti_veri`, `almeno_uno_vero`, `prossimo_elemento` e altri. Le parole `testo`, `lista`, `lunghezza`, `somma`, `tipo`, `genitore`… sono ora libere come nomi di variabile. Codice, esempi, lezioni ed esercizi sono stati aggiornati.
- **Il controllo si vede mentre scrivi**: nell'editor gli errori gravi sono sottolineati in rosso, gli avvisi in arancione, con il motivo nel suggerimento sul mouse e il primo errore nella barra di stato (Impostazioni → Editor → «Sottolinea gli errori gravi»). L'assistente AI riceve gli stessi errori da `controlla_sintassi` e le sue scritture con errori gravi nuovi gli vengono rimandate da correggere. Nuova pagina di aiuto «I trabocchetti più comuni».
- I messaggi d'errore spiegano le parole inglesi (`pass` → `passa`) e «Forse intendevi» è in italiano.
- `pitonit/tools/verifica_tutto.py` esegue tutte le verifiche prima di una release.

## Novità della 1.50

- **Stampa e PDF**: il componente **Stampa** produce un PDF (A4, verticale o orizzontale) con il contenuto di un Albero, un Elenco, un'AreaTesto, un'Etichetta, un Grafico, una Tela (il disegno) o un'Immagine, con titolo, intestazione, data e «Pagina X di Y»; si può guardare (`anteprima()`), salvare (`salva_pdf()`) e stampare (`stampa()`). Le tabelle lunghe vanno su più pagine con l'intestazione ripetuta. Il PDF è scritto da PitStudio, senza librerie esterne (file `stampante.pit` nel progetto, con la classe `Documento` per i documenti fatti a mano); funziona anche nell'esportazione in Python e nell'eseguibile.

## Novità della 1.50 (impostazioni di stampa)

- **Tutte le impostazioni di stampa**: stampante (elenco di quelle installate), copie e fascicola, formato della carta (A3, A4, A5, B5, Letter, Legal), orientamento, margini sui quattro lati, dimensione del testo in %, pagine da stampare (`1-3, 5, 7-`), fronte-retro, colore o bianco e nero, qualità. Si scelgono nelle proprietà del componente Stampa o da codice (`imposta(...)`), e una **finestra di stampa** (anche con il pulsante **Preferenze…** del driver, su Windows) si apre da codice con `finestra_stampa()` o prima di ogni stampa con la proprietà «Mostra la finestra di stampa prima di stampare». Le scelte dell'utente si possono ricordare. Funziona anche nell'esportazione in Python.

## Novità della 1.49

- **Componente Grafico**: barre, linee e torta disegnati con tkinter (nessuna libreria esterna), con titolo, valori, colore e legenda della torta. I dati si scrivono nell'ispettore (`etichetta=valore`) oppure arrivano da una tabella tramite la fonte dati (colonna delle etichette e colonna dei valori) e il grafico si aggiorna quando cambiano. Funziona nel progettista, nel programma, nell'esportazione in Python e nell'eseguibile.

## Novità della 1.48

- **Guide di allineamento** nel progettista: trascinando un componente compaiono linee rosa quando un bordo o il centro coincide con quello di un altro componente (o del contenitore) e il componente si aggancia; casella **Guide** nella barra, Alt per non agganciare. («Distribuisci in modo uniforme» c'era già nel menu Allinea.)

## Novità della 1.47

- **Controllo delle variabili omonime**: l'editor evidenzia con uno sfondo colorato la parola dove un nome ne nasconde un altro (parametro o variabile locale con lo stesso nome di una del modulo o della funzione che la contiene, variabile con lo stesso nome di una funzione o classe, nome di una funzione del linguaggio che poi chiami). Il suggerimento al passaggio del mouse dice cosa nasconde. Non blocca nulla e si spegne in Impostazioni → Editor. **F2** avvisa quando rinomini un nome omonimo.

## Novità della 1.46

- **Salvataggio di sicurezza**: ogni 30 secondi PitStudio copia in `~\.radecupero` i file con modifiche non salvate (editor e finestre del progettista, senza toccare i file). Dopo una chiusura improvvisa, alla riapertura propone di ripristinarli. Le copie spariscono quando salvi o chiudi la scheda. Si regola in Impostazioni → Editor.

## Novità della 1.45

- **Modelli di finestra** in *Nuova finestra*: finestra vuota, **accesso**, **scheda anagrafica con database** (crea il database SQLite e la maschera), **impostazioni a schede**, **ricerca con elenco**. Sono già a griglia, con i gestori degli eventi e un codice d'esempio che funziona; si cambiano nel progettista.

## Novità della 1.44

- **Albero dei componenti** nel progettista (pannello STRUTTURA sotto la palette): la gerarchia di finestra, riquadri e pagine di schede; si seleziona un componente anche se è coperto da altri, la selezione è la stessa nei due posti e si trascinano le righe per spostare un componente in un altro contenitore.
- La lista dei componenti ha ora la barra di scorrimento.
- **Corretto**: una casella di spunta cambiava colore da spuntata se un'altra parte del programma ne impostava `selectcolor`.

## Novità della 1.43

- **Rettangolo di selezione**: trascinando il mouse su uno spazio vuoto si selezionano i componenti toccati (Maiusc = aggiungi), utile per allinearli.
- **Spostare dentro e fuori da un riquadro** (o da una pagina di schede) trascinando il componente; la barra di stato dice dove finirà.
- **Caselle di spunta e pulsanti di scelta leggibili in ogni tema** (in PitStudio, nei programmi e nell'anteprima): disegnati da PitStudio, sfondo scuro con scritta e spunta bianche nel tema scuro, chiaro con scritta nera nel tema chiaro.
- **Disposizione a griglia** nel progettista: la finestra, un **Riquadro** o una pagina di **Schede** possono disporre i componenti in celle (riga, colonna, anche su più celle) con colonne e righe che si allargano con la finestra (*pesi*), margine, spazio e allineamento per ogni componente. Nell'ispettore si scelgono le celle; trascinando un componente si evidenzia la cella di arrivo, le frecce lo spostano di una cella. Si passa da *libero* a *griglia* e viceversa senza perdere le posizioni.
- Il programma generato usa `griglia.pit` (messo nel progetto da PitStudio) con lo stesso calcolo del progettista: ciò che vedi è ciò che ottieni, anche ridimensionando. Funziona nell'esportazione in Python e nell'eseguibile. Le finestre esistenti restano libere.

## Novità della 1.42

- **Corretto**: «Crea l'eseguibile» e «Esporta come Python» da PitStudio.exe si fermavano subito con «module 'os' has no attribute '__file__'» (l'interprete incorporato non ha quel dato): ora usano `sysconfig`. L'autotest di PitStudio.exe prova anche l'esportazione, e con `RAD_PROVA_EXE=1` la costruzione vera dell'exe e del Setup.
- **Corretto**: l'esportazione in Python scambiava per l'operatore «e» (and) una variabile che si chiama `e` scritta dopo `in` (`per x in e["a"]`), e il programma non si convertiva.
- **Database negli exe**: un programma costruito con una fonte dati SQLite perdeva le modifiche alla chiusura (con l'exe a file singolo il database sta in una cartella temporanea). Ora alla prima apertura il database si copia in `%APPDATA%\<nome del programma>` e si usa la copia: le modifiche restano. Prima di costruire, PitStudio rinnova una vecchia `fonte_dati.pit` del progetto.
- **Dati di un programma costruito**: la barra di navigazione ha, nell'exe, il menu **Dati ▾**: mostra dove sta il database, **apre la cartella dei dati**, fa una **copia di sicurezza** e **ripristina da una copia** (con controllo del file e copia automatica dei dati di prima). In *Crea l'eseguibile* si sceglie dove tenere il database: nella cartella dell'utente (consigliato) o accanto al programma (versione portatile).
- **Database spostato**: se il file `.db` non sta dove la finestra lo cerca, il programma lo trova in `risorse/` o nelle sottocartelle; prima di costruire l'exe, PitStudio scrive dove lo ha trovato o avvisa se manca.
- **Spunte e pulsanti di scelta nel tema scuro**: prima la spunta ✓ era quasi invisibile (grigio chiaro su grigio chiaro), adesso si vede in tutta l'applicazione.
- **Distribuzione dei programmi** (*Crea l'eseguibile*): le **informazioni di versione** (nome, versione, autore, descrizione, © autore) finiscono nell'`.exe` e si vedono in *Proprietà → Dettagli*; la spunta **Crea anche il programma di installazione** produce `Setup_<nome>.exe` (scelta della cartella, collegamenti, voce in *App* di Windows e disinstallazione, senza permessi di amministratore, fatto con PyInstaller: nessuno strumento esterno); la **firma facoltativa** con signtool (certificato `.pfx`, password mai salvata né scritta nel registro, marca temporale). La guida spiega anche i limiti dei certificati e l'avviso SmartScreen.

## Novità della 1.41

- **Barra**: chi aveva già una barra personalizzata riceve una volta sola il pulsante «Console» accanto all'assistente (se poi lo toglie, non ricompare).
- **Debug didattico**: quando il programma è fermo, il pannello mostra in blu **come si calcola la riga** che sta per essere eseguita, un passo alla volta (`a + b * 2 → 3 + 8 → 11`, con Vero/Falso in italiano), senza eseguire le tue funzioni. Variabili ed espressioni **cambiate dall'ultima sosta** sono in arancione.
- **Watchpoint**: doppio clic su una espressione osservata (compare 👁) e **Continua** si ferma appena il suo valore cambia («totale è cambiata: 0 → 10 (dopo la riga 4)»), anche quando la variabile viene creata o la funzione finisce. I punti di arresto valgono comunque.

## Novità della 1.40

- **Finestra d'avvio**: all'apertura di PitStudio compare «Che cosa vuoi fare?»: aprire l'ultimo lavoro, iniziare un nuovo progetto o iniziare una lezione di apprendimento, più l'elenco dei progetti recenti. La casella «Non chiedere più» riporta il comportamento di prima (si riapre subito l'ultimo lavoro); la finestra si riapre da *File → Finestra di avvio…*. Con una cartella sulla riga di comando si apre quella e basta.
- **Lezioni con quiz**: *Aiuto → Lezioni (con quiz e professore)…* mostra le 16 lezioni con i progressi (✔ con almeno l'80%). Ogni lezione ha un quiz a risposte multiple (93 domande in tutto, 51 del tipo «Che cosa stampa?» con il codice verificato eseguendolo) con un indizio per ogni errore e la sezione da rileggere. Funziona anche senza AI.
- **Barra**: nuovo pulsante «Console» accanto all'assistente, per mostrare e nascondere la console; come l'assistente è verde quando il pannello è aperto.
- **Corretto**: «Mostra in Esplora risorse» nel menu del pannello Progetto dava un errore (modulo non importato).
- **Quiz**: ogni risposta è un pulsante e quella scelta si colora per intero (prima il pallino, nel tema scuro, non si vedeva); la giusta diventa verde e la sbagliata scelta rossa. Le risposte si scelgono anche da tastiera (tasti 1-9, frecce su/giù, Invio per controllare).
- **Professore AI**: con l'AI configurata (Claude, Gemini o DeepSeek) la chat può fare da professore della lezione: spiega, fa domande, legge il codice dell'allievo e dà indizi, ma non scrive né modifica file. Senza AI la finestra delle lezioni porta alle Impostazioni → Assistente AI (si apre sulla pagina giusta).

## Novità della 1.39

- **Assistente AI con più fornitori**: oltre a Claude (che resta il predefinito) si possono usare **Gemini** (Google) e **DeepSeek**. In *Impostazioni → Assistente AI* si sceglie il fornitore e si mette la sua chiave API (o la variabile `GEMINI_API_KEY` / `DEEPSEEK_API_KEY`). Ogni fornitore ha il suo modello e il suo modello economico; la casella dei modelli nella chat segue il fornitore. L'assistente usa gli stessi strumenti con tutti e tre. La cache dei prompt è solo di Claude, e la stima dei costi si calcola solo per i modelli di cui si conosce il prezzo.
- **Chat**: a ogni richiesta mostra sempre il modello usato, «(modello: …)» o «(modello economico: …)».
- **Cambio di fornitore a metà chat**: si può passare da Gemini o DeepSeek a Claude senza errore (le firme di Gemini e il ragionamento di DeepSeek non vengono più inviati a Claude).
- **Gemini**: modelli aggiornati a `gemini-3.6-flash` (economico `gemini-3.5-flash-lite`), perché i 2.5 non sono più disponibili per i nuovi utenti. Chi li aveva già salvati passa in automatico ai successori.
- **Impostazioni**: le pagine ora scorrono (rotella e barra a destra) quando le voci non ci stanno, così si raggiungono tutte le opzioni dell'Assistente AI.
- **Chat**: la casella «⚡ economico» parte attiva.
- **Barra**: il pulsante dell'assistente è verde quando la chat è aperta e del colore normale (nero nel tema chiaro) quando è chiusa.

## Novità della 1.38

- **Progetto**: una finestra disegnata è un solo nodo dell'albero (🪟 nome) che si apre sui suoi tre file (`<nome>.form.json`, `<nome>_ui.pit`, `<nome>.pit`). Doppio clic sul nodo apre il progettista. *Elimina* sul nodo mostra una finestra con tre spunte (tutte attive) per scegliere quali file togliere; *Rinomina* sul nodo rinomina i tre file e aggiorna il nome della finestra, le classi e le importazioni. Su un singolo file dentro il nodo, Elimina e Rinomina agiscono solo su quel file.
- **Progettista › Proprietà**: il carattere non è più un testo libero. Un elenco con i caratteri installati nel sistema, la dimensione, e le caselle G (grassetto), C (corsivo), S (sottolineato), B (barrato). I file già salvati restano validi.
- **Editor**: nei file di una finestra disegnata, `se_stesso.` propone i componenti con il loro tipo; dopo il nome del componente propone i suoi metodi; dentro le parentesi propone gli argomenti (`se_stesso.etichetta1.configura(` → `testo=`, `sfondo=`, `stato=`…). Per cambiare un componente si scrive `se_stesso.<nome>.configura(testo="Ciao")`; `radice.elementi` non serve.
- **Dati › Struttura**: «✎ Modifica colonna…» (anche con il doppio clic su una riga) cambia nome, tipo, «non nulla» e valore predefinito di una colonna esistente. L'anteprima mostra le istruzioni SQL; in SQLite la tabella si ricostruisce in una transazione (se qualcosa non va, tutto torna com'era; indici, trigger, viste e chiavi esterne restano). Le tabelle con CHECK, COLLATE o unicità su più colonne si rifiutano con un messaggio che manda alla scheda SQL.

## Novità della 1.37

- **Aggiornamento su Linux e macOS**: a fine aggiornamento si tolgono le cartelle temporanee (i sorgenti scompattati e il file scaricato), che prima restavano in `/tmp`.

## Novità della 1.36

- **Correzione all'avvio**: l'elenco delle librerie online cercava `os.__file__`, che nell'interprete incorporato in `PitStudio.exe` non esiste: PitStudio si apriva e si chiudeva subito. Ora usa `sysconfig`.
- **Finestre con i dati**: la copia di `fonte_dati.pit` nel progetto si aggiorna da sola al salvataggio quando è più vecchia di quella di PitStudio (la vecchia resta come `fonte_dati.pit.bak`): prima «Prova» non mostrava Conferma, Annulla tutto e il contatore. L'anteprima della barra di navigazione nel progettista ora è uguale a quella in esecuzione (ricerca a destra con «Tutti»).
- **Anteprima dal vivo**: se una finestra è in prova (▶ Prova) e cambi qualcosa nel progettista (o annulli/ripeti), la prova si riavvia da sola dopo 0,8 secondi, con le modifiche salvate, e la finestra riappare nello stesso punto dello schermo (la finestra provata ricorda dove l'hai messa, anche tra una prova e l'altra).
- La barra di navigazione nel progettista ha le stesse larghezze di quella in esecuzione (misurate sui pulsanti veri).
- **Linux (Debian/Ubuntu)**: `installa.sh` controlla le dipendenze di compilazione e, se mancano, le installa da solo con `sudo apt` (chiede conferma e la password); prima si limitava a stamparti il comando.
- **Linux e macOS**: `sh installa.sh --disinstalla` toglie pytonIta (cartella di installazione e voce nel menu, con conferma; non serve il repository); con `--tutto` anche le impostazioni in `~/.rad`. I progetti non si toccano mai.

## Novità della 1.35

- **Linux (e, da provare, macOS)**: l'interprete pitonit compila con `./configure && make` (la patch aveva una sola chiamata solo Windows, `_wcsicmp`, ora corretta) e **PitStudio gira su Linux**: provato su Ubuntu 24.10 con tutti i 62 test. Nuovo `installatore/linux/installa.sh`: scarica CPython, applica la patch, compila, installa PitStudio e le librerie italiane, crea il comando `pitstudio` e la voce nel menu (opzioni `--prefisso`, `--scientifiche`, `--solo-pitstudio`). Istruzioni in `installatore/linux/LEGGIMI.md` e nella pagina della guida «pytonIta su Linux e macOS».
- **Nuovo modulo `rad/piattaforma.pit`**: caratteri per sistema (al posto di «Segoe UI» e «Consolas» scritti a mano), apertura di file e cartelle, terminale, cursori di ridimensionamento, rotella del mouse (X11), arresto dell'albero di processi.
- I limiti di memoria ai programmi funzionano anche su Linux; il pulsante *Controlla aggiornamenti* su Linux e Mac riscrive PitStudio dai sorgenti della Release senza ricompilare l'interprete.
- Gli strumenti di conversione (`py2pit`, `pit2py`) trovano da soli la `Lib` dell'interprete in uso.

## Novità della 1.34

- **Zona `librerie/` nel repository**: i moduli italiani attuali (108 librerie, 152 file) con un indice (`librerie/indice.json`, con versione e impronta SHA-256 di ogni file) e lo script `librerie/costruisci_indice.py` che lo ricostruisce. Istruzioni in `librerie/LEGGIMI.md`.
- **Librerie online** nel pannello Librerie: **⟳ Novità** legge l'indice e segna ⬆ (versione diversa) e ✚ (nuova); **Installa / Aggiorna**, **Aggiorna tutte** e **Ripristina**. Le copie scaricate vanno in `~/.rad/librerie`, che pitonit cerca *prima* della sua `Lib` (nuovo `sitecustomize.py`); ogni file è verificato con la sua impronta. Logica in `rad/librerie_online.pit`; test: `tests/prova_librerie_online.pit`, `tests/prova_librerie_pannello.pit`.
- **Aggiornamenti di PitStudio**: *Aiuto → Controlla aggiornamenti…* legge l'ultima Release su GitHub, mostra le novità e scarica l'installatore (solo da GitHub, impronta verificata), poi chiude PitStudio e lo avvia dopo la tua conferma. Una volta al giorno, all'avvio, un controllo silenzioso (si disattiva in *Impostazioni → Aggiornamenti*). Logica in `rad/aggiornamenti.pit`; test: `tests/prova_aggiornamenti.pit`, `tests/prova_aggiornamenti_ui.pit`.
- Nuova pagina della guida «Aggiornamenti e librerie online».

## Novità della 1.33

- **Debugger più completo**: punti di arresto **con condizione** (`i > 10`), **dal passaggio N** e **punti di registrazione** (scrivono un messaggio con `{variabili}` senza fermarsi), da un clic destro sul margine; scegliendo una riga della **pila delle chiamate** si vedono le variabili e le espressioni osservate di quella funzione; le espressioni osservate e i punti con condizione restano salvati con il progetto. Test: `tests/prova_debug_condizioni.pit`.
- **Pannello Test**: trova da solo `test_*`, `prova_*`, `*_test` e i file in `tests/`, li esegue (tutti, i selezionati o solo i falliti) con limite di tempo e mostra ✔/✘/⏱ e l'output, con link alle righe degli errori. Test: `tests/prova_pannelli.pit`.
- **Pannello Git**: stato, prepara/togli/annulla, commit (con differenze colorate), storia, rami, pull e push; `git init` con `.gitignore`. Logica in `rad/git_uso.pit` (test: `tests/prova_git.pit`).
- **Pannello Pacchetti (pip)**: installa, aggiorna e toglie i pacchetti di PyPI nell'**ambiente del progetto** (`.pacchetti`, visto da tutti i programmi lanciati da PitStudio tramite `PITONIT_PERCORSI` e il nuovo `sitecustomize.py` del runtime) o nel runtime di pitonit; cerca gli aggiornamenti; scrive e installa `requirements.txt`. Test: `tests/prova_pacchetti.pit`.
- Quattro nuove pagine della guida (debugger aggiornato, «I test del progetto», «Git», «I pacchetti Python»).

## Novità della 1.32

- **Commit e rollback** per le finestre con i dati: la proprietà **Modifiche in sospeso** (`transazione`) della fonte dati lascia ogni salvataggio ed eliminazione in una transazione del database. Diventano definitivi solo con **Conferma** (`fonte1.conferma()`), si cancellano tutti con **Annulla tutto** (`fonte1.annulla_tutto()`); `fonte1.modifiche_in_sospeso()` dice quante ce ne sono. Nuovi pulsanti opzionali della barra (*Conferma*, *Annulla tutto*) e la scritta «3 / 25 · 2 non confermate»; chiudendo la finestra con modifiche in sospeso chiede se confermare, annullare o restare. SQLite e MySQL.
- **Albero modificabile** (proprietà *Modificabile*): doppio clic (o F2) su una cella per scriverci, Invio/Tab confermano, Insert aggiunge una riga da compilare, Canc elimina. Le righe cambiate e non confermate sono evidenziate in giallo: si possono modificare molti record e poi confermarli o annullarli in blocco. Test: `tests/prova_transazione.pit`.

## Novità della 1.31

- **Salvataggio automatico** dei campi legati ai dati: prima si salvava solo con il pulsante «Salva» della barra, quindi un campo legato senza barra non scriveva nulla nel database. Ora la fonte dati salva da sola le modifiche cambiando record, cercando, aggiungendo un record nuovo e chiudendo la finestra (proprietà **Salva da solo** della fonte dati, accesa di default). Un record nuovo lasciato vuoto non viene aggiunto.

## Novità della 1.30

- **Dati nelle finestre**: due nuovi componenti nel progettista, **FonteDati** (database SQLite o MySQL, tabella, filtro, ordine; le tabelle e le colonne si scelgono da elenchi presi dal database vero) e **BarraNavigazione** (primo, precedente, successivo, ultimo, nuovo, salva, elimina, annulla, ricerca e «3 / 25», con i pulsanti scelti uno per uno). Campi, caselle, aree di testo, cursori, caselle combinate, etichette, elenchi e alberi hanno le proprietà **Fonte dati** e **Campo**: mostrano il record corrente e lo salvano senza scrivere codice. Le maschere automatiche (*Database → Crea una maschera dalla tabella…*) ora sono costruite con questi componenti e si modificano nel progettista. Funziona con l'esportazione in Python e la creazione dell'eseguibile. Guida: «Dati nelle finestre». Test: `tests/prova_dati_form.pit`.
- **Caselle di spunta leggibili**: nel tema scuro la spunta era nera su grigio scuro e non si capiva se la casella fosse attiva; ora la casella è chiara (proprietà del progettista, impostazioni, esportazione e altre finestre).

## Novità della 1.29

- **Aspetto moderno** delle finestre che crei: la proprietà **Aspetto** della finestra (classico, chiaro, scuro, verde, viola) dà colori coordinati, caratteri Segoe UI, campi con bordo sottile, pulsanti piatti, tabelle, schede e barre nello stesso stile, con anteprima fedele nel progettista. I colori scelti a mano hanno la precedenza. Nessuna libreria esterna: PitStudio aggiunge al progetto il file `aspetto.pit`. Le maschere e gli esempi della galleria lo usano.

## Novità della 1.28

- **Per chi impara**: la **Galleria di esempi** (11 progetti pronti: console, finestre, database; si copiano in un nuovo progetto e si provano) e gli **Esercizi guidati** (13 esercizi con controllo automatico del codice, suggerimenti, soluzione e progressi). Per le classi: gli allievi **esportano i progressi** in un file, l'insegnante ne ottiene il **report della classe** e può aggiungere **esercizi propri** (file `.json`). Entrambi si aprono dal menu *Aiuto* e dalla schermata di benvenuto.
- Corretto: un carattere scritto come «Segoe UI 14 bold» nel progettista faceva fallire la finestra generata.

## Novità della 1.27

- **Editor: navigazione nel codice**: *Vai alla definizione* (F12 o Ctrl+clic), *Trova gli usi* (Maiusc+F12), *Rinomina in tutto il progetto* (F2, anche nei gestori dei form), **documentazione al passaggio del mouse** su funzioni del progetto e parole del linguaggio, *Ripulisci il codice* (Ctrl+Maiusc+L) e **menu con il clic destro**. Lavora sui file `.pit` e `.py` leggendo i «token»: non confonde i nomi con testi e commenti.

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
