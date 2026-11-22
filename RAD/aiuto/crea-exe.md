# Creare un eseguibile (.exe)

Un programma pytonIta gira dentro PitStudio. Per darlo a chi **non ha né PitStudio né Python**, PitStudio ne fa un **eseguibile Windows** (`.exe`): un solo file da copiare e avviare con un doppio clic.

## Come si fa

1. Apri il progetto e scegli *File → Crea l'eseguibile (.exe)…* (o *Progetto → Crea l'eseguibile (.exe)…*).
2. Controlla le opzioni:
   - **Nome del programma**: è il nome del file `.exe`.
   - **Icona**: un file `.ico` (facoltativa).
   - **Un solo file .exe**: comodo da spedire; parte un po' più lentamente. Senza la spunta ottieni una cartella con l'`.exe` e i suoi file.
   - **Senza finestra nera**: lascia la spunta per i programmi con finestre; toglila per i programmi da console (quelli che usano `leggi_tastiera()` e `stampa()`).
   - **Versione, autore, descrizione**: finiscono nelle *informazioni del file* (clic destro sull'`.exe` → *Proprietà* → *Dettagli*): nome del prodotto, versione, autore/azienda e «© autore». PitStudio ricorda le tue scelte nel progetto.
   - **Crea anche il programma di installazione**: vedi sotto.
   - **Firma**: facoltativa, vedi sotto.
3. Premi **Crea l'eseguibile** e guarda il registro. Alla fine premi **Apri la cartella**.

Il risultato è nella cartella **`dist`** del progetto.

## Se il programma usa un database

Un programma con una **fonte dati SQLite** (maschere collegate a un `.db`) porta il database dentro il pacchetto. Con l'exe a file singolo il pacchetto si scompatta in una cartella temporanea a ogni avvio e si cancella alla chiusura, quindi PitStudio fa così: **alla prima apertura copia il database nella cartella dei dati dell'utente** (`%APPDATA%\<nome del programma>\`) e da quel momento usa la copia. Le modifiche restano da un avvio all'altro, e ogni utente di Windows ha i suoi dati. Il database del pacchetto resta com'era, come punto di partenza. Nel progetto dentro PitStudio non cambia niente: si usa il file del progetto.

- **Dove tenere il database**: nella finestra *Crea l'eseguibile* scegli *«nella cartella dell'utente (consigliato)»* oppure *«accanto al programma (versione portatile)»*. La seconda serve per portare programma e dati su una chiavetta; richiede una cartella dove si può scrivere (se non si può, il programma ripiega da solo sulla cartella dell'utente).
- **Il menu «Dati»**: nei programmi costruiti, la **barra di navigazione** ha un menu **Dati ▾** che dice dove sono i dati («Dati in: …») e permette di **aprire la cartella dei dati**, **creare una copia di sicurezza** (un file `.db` con la data nel nome, da salvare dove vuoi, per esempio su una chiavetta) e **ripristinare da una copia**. Prima di un ripristino il programma salva da solo i dati di adesso accanto al database, così si può tornare indietro; controlla anche che il file sia davvero una copia di questi dati. La copia e il ripristino non si fanno se ci sono modifiche non confermate. Il menu compare solo nell'exe (dentro PitStudio non serve); si può togliere con la proprietà **Menu «Dati»** della barra nel progettista.
- Con **accanto al programma** il file del database **non compare in `dist` finché non avvii il programma**: nasce al primo avvio, accanto all'`.exe`, e da lì in poi resta.
- Se il database non sta nella cartella del progetto dove la finestra lo cerca (per esempio lo hai spostato in `risorse/`), il programma lo cerca anche in `risorse/` e nelle sottocartelle (fino a 3 livelli). Prima di costruire, PitStudio scrive nel registro dove lo ha trovato oppure ti **avvisa** se non lo trova (altrimenti il programma direbbe «Il database non esiste»).
- Per **ripartire da zero** basta cancellare la cartella dei dati.
- Il database è quello della **prima installazione**: una nuova versione del programma con tabelle cambiate non aggiorna da sola il database già copiato.
- Se la copia di `fonte_dati.pit` del progetto è vecchia, PitStudio la rinnova prima di costruire (la vecchia resta come `fonte_dati.pit.bak`).
- MySQL non è toccato: i dati stanno sul server.

## Il programma di installazione (Setup)

Con la spunta **Crea anche il programma di installazione** ottieni, oltre all'`.exe`, un secondo file **`Setup_<nome>.exe`**: è quello da spedire. Chi lo apre vede una finestra con il nome e la versione del programma, sceglie la cartella (di solito `%LOCALAPPDATA%\Programs\<nome>`), decide se creare i collegamenti sul desktop e nel menu Start e preme **Installa**. Non servono i permessi di amministratore.

- Il programma installato compare in **Impostazioni → App** di Windows, e da lì si **disinstalla** (c'è anche il collegamento «Disinstalla» nel menu Start). I file che l'utente ha creato con il programma non vengono toccati.
- Il Setup è fatto da PitStudio con lo stesso PyInstaller: non serve installare altro (né Inno Setup né simili).
- Per provarlo senza finestra: `Setup_<nome>.exe /S --cartella=C:\Prova --senza-collegamenti`.

## Firmare i file (facoltativo)

Windows mostra l'avviso «**editore sconosciuto**» (SmartScreen) per i programmi non firmati. Per toglierlo servono un **certificato di firma del codice** e `signtool.exe` (si installa con il *Windows SDK*, componente «Strumenti di firma»). In PitStudio: spunta **Firma i file**, scegli il file `.pfx` del certificato e scrivi la sua password. PitStudio firma l'`.exe` e il Setup (con la marca temporale, così la firma resta valida dopo la scadenza del certificato). La **password non viene salvata** né scritta nel registro.

Cose da sapere sui certificati:

- Un certificato **autofirmato** non toglie l'avviso: Windows non si fida di chi lo ha fatto.
- I certificati di una autorità riconosciuta si pagano; anche con un certificato nuovo, SmartScreen può avvisare finché il programma non ha «reputazione».
- Per i progetti **open source** esiste la *SignPath Foundation*, che firma gratis i progetti che rispettano le sue regole (licenza OSI, repository pubblico, build automatiche). Il certificato è della Fondazione, non tuo.
- Se la firma non riesce, l'`.exe` resta creato (non firmato) e PitStudio te lo dice.

## Che cosa succede

PitStudio fa quattro passi, e li racconta uno per uno:

1. converte il progetto in Python (come *Esporta il progetto come Python*);
2. prepara l'ambiente di costruzione dentro `.rad/build` del progetto;
3. vi installa **PyInstaller** e le librerie che il programma usa (`requirements.txt`);
4. costruisce l'`.exe` con PyInstaller.

Per costruire PitStudio usa **il proprio interprete** (pitonit, lo stesso con cui esegui i programmi): **non serve installare Python**. Dalla finestra, *Costruisci con* permette di scegliere invece il Python 3 installato sul computer, per esempio se ti serve una versione precisa.

Il tuo computer non viene toccato: tutto avviene in quella cartella, che puoi cancellare quando vuoi.

## Cosa serve

- Nient'altro che PitStudio: l'interprete di PitStudio costruisce l'eseguibile. (Solo se scegli *il Python 3 installato sul computer* serve [Python](https://www.python.org/downloads/), con la spunta «Add python.exe to PATH».) Chi riceve l'`.exe` **non** ha bisogno di nulla.
- **Internet la prima volta**, per scaricare PyInstaller e le librerie. Le volte dopo l'ambiente è già pronto e la costruzione è molto più veloce.

## Se il programma costruito ha un errore

Un programma «senza finestra nera» che va in errore, di norma, si chiude e basta: nessuno sa perché. Per questo ogni eseguibile costruito da PitStudio **parte da un piccolo avvio** che sta intorno al tuo programma (non ne cambia il comportamento):

- un errore non gestito, anche dentro un **filo** o dentro un **pulsante** di una finestra, viene scritto nel file **`errori.log`** con data, nome e versione del programma, sistema e traceback completo;
- nei programmi senza finestra nera compare un **avviso** con il percorso del registro e la domanda se aprire la cartella; un errore nel pulsante lascia il programma aperto (l'avviso non compare più di una volta ogni 10 secondi);
- nei programmi da console l'errore si vede come sempre, e in più resta nel registro;
- `sys.exit(codice)` non è un errore: esce con quel codice senza scrivere nulla.

Il registro è in `%LOCALAPPDATA%\<nome del programma>\errori.log` su Windows e in `~/.local/state/<nome>/errori.log` su Linux; si tronca da solo oltre 1 MB. Chi ti segnala un problema può mandarti quel file. Per provare senza finestre di avviso: variabile d'ambiente `PITSTUDIO_SENZA_AVVISI=1`.

## Cose da sapere

- Le immagini, i file `.json`, i database e gli altri file del progetto vengono inclusi nell'`.exe`. Per trovarli, il programma deve usare il percorso del proprio file (`os.path.dirname(__file__)`) e non il «percorso corrente».
- I file che il programma **crea** (per esempio un database nuovo) finiscono nella cartella da cui viene avviato: con l'opzione «un solo file» l'`.exe` si scompatta in una cartella temporanea a ogni avvio.
- Un eseguibile con le librerie scientifiche (`numpy`, `pandas`, `matplotlib`…) pesa decine di megabyte.
- Windows (o l'antivirus) può avvisare che l'`.exe` «non è firmato»: succede a tutti i programmi che non hanno un certificato a pagamento. Si sceglie «Esegui comunque».
- Se qualcosa non riesce, il registro mostra l'errore di PyInstaller: leggi le ultime righe.
