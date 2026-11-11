# Creare un eseguibile (.exe)

Un programma pytonIta gira dentro PitStudio. Per darlo a chi **non ha né PitStudio né Python**, PitStudio ne fa un **eseguibile Windows** (`.exe`): un solo file da copiare e avviare con un doppio clic.

## Come si fa

1. Apri il progetto e scegli *File → Crea l'eseguibile (.exe)…* (o *Progetto → Crea l'eseguibile (.exe)…*).
2. Controlla le opzioni:
   - **Nome del programma**: è il nome del file `.exe`.
   - **Icona**: un file `.ico` (facoltativa).
   - **Un solo file .exe**: comodo da spedire; parte un po' più lentamente. Senza la spunta ottieni una cartella con l'`.exe` e i suoi file.
   - **Senza finestra nera**: lascia la spunta per i programmi con finestre; toglila per i programmi da console (quelli che usano `leggi()` e `stampa()`).
   - **Versione, autore, descrizione**: finiscono nelle *informazioni del file* (clic destro sull'`.exe` → *Proprietà* → *Dettagli*): nome del prodotto, versione, autore/azienda e «© autore». PitStudio ricorda le tue scelte nel progetto.
   - **Crea anche il programma di installazione**: vedi sotto.
   - **Firma**: facoltativa, vedi sotto.
3. Premi **Crea l'eseguibile** e guarda il registro. Alla fine premi **Apri la cartella**.

Il risultato è nella cartella **`dist`** del progetto.

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
2. prepara un ambiente di costruzione dentro `.rad/build` del progetto;
3. vi installa **PyInstaller** e le librerie che il programma usa (`requirements.txt`);
4. costruisce l'`.exe` con PyInstaller.

Il tuo computer non viene toccato: tutto avviene in quella cartella, che puoi cancellare quando vuoi.

## Cosa serve

- **Python 3** installato sul computer di chi costruisce l'eseguibile (da [python.org](https://www.python.org/downloads/), con la spunta «Add python.exe to PATH»). Chi riceve l'`.exe` **non** ha bisogno di nulla.
- **Internet la prima volta**, per scaricare PyInstaller e le librerie. Le volte dopo l'ambiente è già pronto e la costruzione è molto più veloce.

## Cose da sapere

- Le immagini, i file `.json`, i database e gli altri file del progetto vengono inclusi nell'`.exe`. Per trovarli, il programma deve usare il percorso del proprio file (`os.path.dirname(__file__)`) e non il «percorso corrente».
- I file che il programma **crea** (per esempio un database nuovo) finiscono nella cartella da cui viene avviato: con l'opzione «un solo file» l'`.exe` si scompatta in una cartella temporanea a ogni avvio.
- Un eseguibile con le librerie scientifiche (`numpy`, `pandas`, `matplotlib`…) pesa decine di megabyte.
- Windows (o l'antivirus) può avvisare che l'`.exe` «non è firmato»: succede a tutti i programmi che non hanno un certificato a pagamento. Si sceglie «Esegui comunque».
- Se qualcosa non riesce, il registro mostra l'errore di PyInstaller: leggi le ultime righe.
