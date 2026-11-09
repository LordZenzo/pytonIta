# pytonIta

**Python con le parole chiave in italiano**, e un ambiente di sviluppo scritto nello stesso linguaggio.

```
definisci saluta(nome):
    stampa(f"Ciao, {nome}!")

per i in intervallo(3):
    saluta("mondo")
```

Tre parti, una sola installazione:

| Parte | Cosa è |
|---|---|
| **pitonit** | Un vero interprete CPython 3.13 ricompilato: le parole chiave italiane sono lette dal parser C, non da un traduttore. File `.pit`. Installazione isolata: non tocca Python, il PATH né il registro. |
| **PitStudio** | L'ambiente di sviluppo, scritto in pytonIta: editor con suggerimenti, progetti, progettista di finestre, **programmi a mattonelle** (stile Scratch, con conversione da e verso il codice), debugger, console, assistente AI. |
| **Installatore** | Un solo file `Installa_pytonIta.exe` (Windows): si scompatta in una cartella temporanea, installa e si cancella. Non servono Python né diritti di amministratore. |

## Scaricare

Vai su **Releases** e scarica `Installa_pytonIta.exe`. Windows può mostrare l'avviso SmartScreen perché il file non è ancora firmato: scegli *Ulteriori informazioni → Esegui comunque*.

Viene installato in `%LOCALAPPDATA%\Programs\pytonIta`, con le voci nel menu Start.

## Cartelle del repository

- `pitonit/` — la patch di CPython (`patch/pitonit.patch`), gli strumenti (traduttore `py2pit`, dizionari delle librerie), esempi e documentazione dell'interprete
- `RAD/` — PitStudio (sorgenti `.pit`, guida, test)
- `installatore/` — la costruzione dell'installatore
- `docs/` — la pagina web del progetto

## Domande e contatti

- Domande e idee: [Discussions](https://github.com/LordZenzo/pytonIta/discussions)
- Errori e problemi: [Issues](https://github.com/LordZenzo/pytonIta/issues)
- Senza GitHub: pytonita.progetto@gmail.com
- Pagina web: https://lordzenzo.github.io/pytonIta/

## Licenza

Il software è gratuito da usare, ma **non è modificabile né ridistribuibile in versione modificata**: vedi [LICENSE](LICENSE). Le parti derivate da CPython restano sotto la licenza PSF.
