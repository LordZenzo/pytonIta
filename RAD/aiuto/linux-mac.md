# pytonIta su Linux e macOS

Su Windows c'è l'installatore `Installa_pytonIta.exe`. Su Linux e macOS lo script `installa.sh` **compila l'interprete pitonit dai sorgenti** (CPython 3.13 con la patch di pitonit) e installa PitStudio e le librerie italiane. Non servono privilegi di amministratore: di solito installa in `~/.local/pytonita`.

## Cosa serve prima

Un compilatore C, `make`, `git`, `curl` e le librerie di sviluppo di Tk, OpenSSL, SQLite, zlib e poche altre. Lo script controlla i programmi e, se mancano, stampa il comando per la tua distribuzione.

| Sistema | Comando |
|---|---|
| Ubuntu / Debian | `sudo apt install build-essential git curl python3-tk tk-dev libssl-dev libffi-dev zlib1g-dev libbz2-dev libsqlite3-dev liblzma-dev libreadline-dev uuid-dev` |
| Fedora | `sudo dnf install gcc make git curl tk-devel openssl-devel libffi-devel zlib-devel bzip2-devel sqlite-devel xz-devel readline-devel libuuid-devel` |
| Arch | `sudo pacman -S base-devel git curl tk openssl libffi zlib bzip2 sqlite xz readline` |
| macOS | `xcode-select --install` e `brew install openssl@3 tcl-tk xz sqlite3 readline` |

## Installare

Dalla cartella del repository (`git clone https://github.com/LordZenzo/pytonIta`):

```sh
sh installatore/linux/installa.sh
```

La compilazione richiede da 5 a 15 minuti. Opzioni:

- `--prefisso=/percorso` installa altrove;
- `--scientifiche` aggiunge numpy, pandas, scipy, matplotlib, requests, reportlab, tksheet (da PyPI);
- `--solo-pitstudio` riscrive solo PitStudio e le librerie, senza ricompilare: è quello che usa l'aggiornamento automatico.
- `--disinstalla` toglie pytonIta: la cartella di installazione e la voce nel menu (chiede conferma, non serve il repository). Con `--tutto` toglie anche le impostazioni in `~/.rad`; i tuoi progetti non si toccano mai.

Poi:

```sh
~/.local/pytonita/bin/pitstudio            # apre PitStudio
~/.local/pytonita/bin/pitonit programma.pit  # esegue un programma
```

Su Linux viene creata anche la voce «PitStudio» nel menu delle applicazioni.

## Provare su Linux senza lasciare Windows

Se usi Windows, il Linux di Windows (WSL) ti permette di vedere come si comporta un programma su Linux con un clic: *Esegui → Prova su Linux (WSL)*. Insieme alla verifica del codice è spiegato in [Compatibilità Windows / Linux](#compatibilita-linux).

## Aggiornamenti

*Aiuto → Controlla aggiornamenti* funziona anche qui: scarica i sorgenti della nuova Release, lancia `installa.sh --solo-pitstudio` sull'installazione in uso e propone di riavviare. L'interprete non viene ricompilato: se una versione futura cambia l'interprete, le note della Release lo diranno e basterà rilanciare `installa.sh` per intero.

## Differenze rispetto a Windows

- I limiti di memoria ai programmi eseguiti da PitStudio funzionano su Linux (limite sullo spazio di indirizzamento); il limite sul numero di processi e, su macOS, quello sulla memoria non ci sono.
- «Crea l'eseguibile» produce un programma per il sistema su cui lo costruisci (serve PyInstaller).
- I caratteri sono quelli di sistema (DejaVu su Linux, Helvetica Neue e Menlo su macOS).
- Le icone dei pulsanti sono quelle di ripiego, non «Segoe Fluent Icons».

## Audio e video

I moduli `suono`, `multimedia`, `ffmpeg` e `lettore` funzionano anche qui, con qualche differenza:

- **ffmpeg** non si scarica da PitStudio (il download automatico c'è solo su Windows): si installa con il gestore di pacchetti, per esempio `sudo apt install ffmpeg` (Debian/Ubuntu), `sudo dnf install ffmpeg` (Fedora), `sudo pacman -S ffmpeg` (Arch) o `brew install ffmpeg` (macOS). *Strumenti → ffmpeg: audio e video…* mostra il comando adatto al tuo sistema; se ffmpeg è già nel `PATH` lo usa. `ffmpeg.cattura_schermo` è solo per Windows.
- **VLC** (per `lettore` e per la finestra *Strumenti → Lettore audio e video…*) si installa allo stesso modo, per esempio `sudo apt install vlc`; il pulsante «Installa VLC» (winget) c'è solo su Windows. Il video dentro una finestra usa X11 (anche tramite XWayland); su macOS il video dentro una finestra non è ancora supportato.
- **suono** suona i `.wav` con il lettore del sistema (`aplay`, `paplay` o `afplay`); senza scheda audio dà un errore chiaro. `suono.ripeti()` e `suono.avviso()` (il suono di sistema) sono solo per Windows.
- **Stato della verifica**: provato su Ubuntu 24.10 senza ffmpeg né VLC installati (messaggi, ripieghi, comandi, finestre e tutta la serie di test). La parte che richiede ffmpeg e VLC veri su Linux non è ancora stata provata.
