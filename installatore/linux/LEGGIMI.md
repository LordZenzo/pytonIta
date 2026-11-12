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

## Aggiornamenti

*Aiuto → Controlla aggiornamenti* funziona anche qui: scarica i sorgenti della nuova Release, lancia `installa.sh --solo-pitstudio` sull'installazione in uso e propone di riavviare. L'interprete non viene ricompilato. Se la nuova versione ne richiede uno più nuovo (come passando dalla 1.x alla 2.x, che ha cambiato i nomi delle funzioni), lo script se ne accorge, **non cambia nulla** e ti dice di rilanciare `installa.sh` per intero (compila anche l'interprete). Se hai già aggiornato con una versione che non faceva questo controllo e PitStudio non parte più, la soluzione è la stessa: `sh installatore/linux/installa.sh` dalla cartella del repository. Le tue impostazioni (`~/.rad`) e i tuoi progetti non si toccano.

## Differenze rispetto a Windows

- I limiti di memoria ai programmi eseguiti da PitStudio funzionano su Linux (limite sullo spazio di indirizzamento); il limite sul numero di processi e, su macOS, quello sulla memoria non ci sono.
- «Crea l'eseguibile» produce un programma per il sistema su cui lo costruisci (serve PyInstaller).
- I caratteri sono quelli di sistema (DejaVu su Linux, Helvetica Neue e Menlo su macOS).
- Le icone dei pulsanti sono quelle di ripiego, non «Segoe Fluent Icons».
