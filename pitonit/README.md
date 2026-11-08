# pitonit — Python con l'interprete in italiano

Un vero interprete CPython 3.13 ricompilato: le parole chiave italiane sono
riconosciute **dal parser C**, non da un traduttore a monte. File: `.pit`.

## Installazione separata (nessun conflitto con Python)
`installazione\` è autonoma: `pitonit.exe`, `Lib\`, `DLLs\`.
- `pitonit._pth` isola l'interprete: ignora `PYTHONHOME`, `PYTHONPATH` e il registro di Python.
- Non scrive nel registro e non tocca il PATH.
- Opzionale: `registra_pit.cmd` associa i `.pit` a pitonit (solo utente corrente); `annulla_registrazione_pit.cmd` lo toglie.

```
installazione\pitonit.exe esempi\base.pit
installazione\pitonit.exe            (console interattiva)
installazione\pitonit.exe -c "stampa('ciao')"
```
I file `.py` eseguiti con pitonit restano Python normale (inglese).

## Cosa è stato modificato in CPython (`patch\pitonit.patch`)
| Dove | Cosa |
|---|---|
| `Parser/pegen.c` | Flag `PyPARSE_ITALIANO`: parole chiave italiane (`se`, `altrimenti_se`, `per`, `definisci`, `ritorna`, `classe`, `importa`, `prova/eccetto/infine`, `e/o/non`, `è`, `Vero/Falso/Nessuno`, `confronta/caso/tipo`...). In modalità italiana le parole inglesi non sono riservate. `e`/`o` sono operatori solo tra due operandi (si può scrivere `eccetto X come e`). Metodi speciali: `__inizializza__`→`__init__` ecc. |
| `Parser/pegen.c` (nomi) | Le parole riservate come `classe`, `con`, `da`, `prova`, `elimina` si leggono come nomi dove una parola chiave non può comparire (vedi `NOMI.md`); `e`/`o` a fine riga continuano la condizione. |
| `Python/bltinmodule.c` (`_imposta_nel_tipo`), `Lib/_italiano.py` | Opzioni con nome in italiano (`chiave=`, `inverso=`, `codifica=`…) e altri messaggi d'errore tradotti. |
| `Include/cpython/compile.h` | `PyCF_ITALIANO` (0x10000), salvato in `co_flags`: `esegui`/`valuta`/`compila` lo ereditano. |
| `Modules/main.c` | File `.pit`, `-c`, stdin e console sono italiani; banner e `--version` «Pitonit». |
| `Python/bltinmodule.c` | `esegui`/`valuta` usano i builtin italiani; `_aggiungi_alias` per i metodi. |
| `Lib/importlib/_bootstrap_external.py` | `import` trova e compila i moduli `.pit` (italiani). |
| `Lib/_italiano.py` | Builtin italiani (`stampa`, `lunghezza`...), eccezioni (`ErroreDiValore`...), alias dei metodi (`lista.aggiungi`, `testo.maiuscolo`...), errori e traceback tradotti, `Vero/Falso/Nessuno` nell'output. |
| `Lib/matematica.py`, `casuale.py`, `tempo.py`, `sistema.py`, `sistema_operativo.py`, `collezioni.py`, `percorso.py`, `espressioni_regolari.py`, `funzioni_utili.py`, `iteratori.py`, `dati_classe.py`, `formato_json.py` | Moduli standard con nomi italiani (restano disponibili anche i nomi originali). |

La libreria standard resta in inglese e funziona normalmente (viene compilata in modalità inglese).

## Ricompilare
Servono Visual Studio 2022 (C++) e git. Da `src\`:
```
PCbuild\build.bat -p x64 -c Release --no-tkinter
python ..\tools\installa.py
```
(`src\` è un clone di CPython ramo 3.13 con la patch applicata.)

## Librerie in italiano
152 moduli (`ELENCO_LIBRERIE.md`, circa 8.700 alias): tkinter (`interfaccia`, `interfaccia.tema`, ...), ctypes (`tipi_c`), reportlab
(`rapporti_pdf`), datetime (`data_ora`), sqlite3 (`database`), shutil, urllib, threading (`thread`), subprocess
(`processi`), argparse (`argomenti`), requests (`richieste`), la libreria standard più comune, numpy (`numerico`),
pandas (`tabelle`), scipy (`scienza`), matplotlib (`grafici`), tksheet, PIL (`immagini`).
I nomi più importanti sono scelti a mano; il resto dell'API pubblica (funzioni, metodi, costanti) è tradotto in automatico dal
glossario `tools\glossario.py` (`ottieni_figli`, `imposta_titolo`...). Le parole che il glossario non conosce finiscono in
`tools
on_tradotti.txt`: aggiungile al glossario e rigenera. Un alias non sovrascrive mai un nome esistente, e non può essere
una parola chiave italiana (per questo `cancella` e `aspetta` al posto di `elimina` e `attendi`).
I dati stanno in `tools\dizionari\*.py`; `python tools\genera_moduli.py` rigenera i moduli, `python tools\installa.py`
li copia, `installazione\pitonit.exe toolserifica_moduli.pit tools\moduli_generati.txt` verifica che ogni alias esista.
Opzioni in italiano (`testo=`, `comando=`, `lato="sinistra"`...), metodi richiamati dalla libreria (`prepara` per
`setUp`, `esegui` per `Thread.run`, `gestisci_GET`...) e messaggi di errore sono tradotti dove ha senso.
Le librerie esterne sono installate dentro pitonit (`pitonit -m pip install ...`), separate da quelle di Python.

## Traduttore py -> pit
`tools\py2pit.py origine.py destinazione.pit` traduce un programma Python: parole chiave (anche `match/case/type`),
costanti e builtin, con analisi degli ambiti (una variabile tua chiamata `id` non viene toccata). Rinomina con `_` gli
identificatori che coincidono con parole italiane riservate (`testo`, `da`, `con`...). Poi **verifica** il risultato:
lo compila con pitonit e confronta la struttura con l'originale. Esempio: `tools\campione\completo.py`.

## Limiti noti
- I builtin hanno nomi italiani **e** inglesi (`stampa` e `print`): il codice generato dalla libreria standard con `exec`
  (dataclasses, namedtuple...) è inglese e deve funzionare. Le parole chiave invece sono solo italiane nei `.pit`.
- `Vero/Falso/Nessuno` appaiono nell'output di `stampa` e della console, anche dentro liste/tuple/dizionari; `repr()`/`testo()` di un booleano restano `True/False` (la libreria standard li usa per generare codice).
- I nomi di metodi/attributi dei tipi base sono tradotti; quelli dei moduli solo per i moduli italiani elencati sopra.
- Messaggi d'errore: tradotti i più comuni (stampa del traceback e di `stampa(errore)`); `testo(errore)` resta inglese.
- Evidenziazione dei colori nella console non conosce le parole italiane.
- Console interattiva (tty) non provata in questa sessione, solo `code.InteractiveConsole` e `_pyrepl` da script.
