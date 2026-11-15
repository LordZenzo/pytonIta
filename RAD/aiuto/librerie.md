# Le librerie in italiano

Ogni libreria di Python ha un **modulo italiano** con gli stessi contenuti e i nomi tradotti. Il nome originale resta sempre valido: puoi mescolare (`importa json` o `importa formato_json`).
I nomi più importanti sono scelti a mano, il resto dell'API è tradotto automaticamente. Per vedere cosa contiene un modulo scrivi `modulo.` nell'editor e guarda i suggerimenti, oppure chiedilo all'assistente.

## Le principali

| Libreria | Modulo italiano | Esempio |
|---|---|---|
| tkinter | `interfaccia` (+ `interfaccia.tema`, `.messaggi`, `.dialoghi_file`) | `tk.Finestra()`, `tk.Pulsante(radice, testo="OK")` |
| os, os.path | `sistema_operativo`, `sistema_operativo.percorso` | `cartella_corrente()`, `percorso.esiste(p)` |
| pathlib | `percorso` | `Percorso("a.txt").leggi_testo()` |
| sys | `sistema` | `sistema.argomenti` |
| datetime | `data_ora` | `OraData.adesso()`, `Data(2026, 1, 31)` |
| time, math, random | `tempo`, `matematica`, `casuale` | `tempo.pausa(1)`, `matematica.radice_quadrata(9)` |
| json, csv | `formato_json`, `tabelle_csv` | `formato_json.carica_testo(t)` |
| sqlite3 | `database` | `database.connetti("dati.db")` |
| re | `espressioni_regolari` | `espressioni_regolari.cerca(modello, testo)` |
| collections | `collezioni` | `contatore(lista).più_comuni(3)` |
| shutil, glob, tempfile | `operazioni_file`, `cerca_file`, `file_temporanei` | `operazioni_file.copia(a, b)` |
| threading, subprocess | `thread`, `processi` | `processi.esegui(["dir"], cattura_output=Vero)` |
| argparse, logging | `argomenti`, `registro` | `registro.informazione("avviato")` |
| urllib, requests | `rete_url`, `richieste` | `richieste.ottieni(url).testo` |
| unittest | `test_unitari` | `classe Prova(test_unitari.CasoDiTest)` |
| asyncio | `asincronia` | `asincronia.esegui(principale())` |
| numpy, pandas, scipy | `numerico`, `tabelle`, `scienza` | `numerico.matrice([1, 2, 3]).media()` |
| matplotlib | `grafici` (`grafici.disegno` = pyplot) | `disegno.traccia(x, y, etichetta="a")` |
| reportlab, PIL | `rapporti_pdf`, `immagini` | `immagini.apri("a.png").ridimensiona((64, 64))` |
| (nostro) | `lettore` | `lettore.Lettore().apri("film.mp4")`, `p.pausa()`, `p.volume = 60` |
| (nostro) | `ffmpeg` | `ffmpeg.apri("a.mp4").ridimensiona(larghezza=640).salva("b.mp4")` |
| (nostro) | `multimedia` | `multimedia.converti("a.wav", "a.mp3")`, `multimedia.info("film.mp4")` |
| (nostro) | `suono` | `suono.riproduci("ciao.wav")`, `suono.suona([("do4", 1), ("mi4", 1)])` |

## Il modulo `suono`

Per i suoni c'è un modulo tutto nostro, senza equivalente in Python: `importa suono`. Suona i file `.wav`, fa dei beep e crea tonalità e piccole melodie.

```pit sintassi
importa suono

suono.riproduci("applauso.wav")                     # suona e aspetta la fine
suono.riproduci("musica.wav", attendi=Falso)        # parte e il programma continua
suono.ferma()                                       # interrompe il suono in corso
suono.beep(880, 0.3)                                # frequenza in hertz, durata in secondi
suono.suona([("do4", 1), ("mi4", 1), ("sol4", 2)])  # note e battute
suono.crea_melodia("brano.wav", [("la4", 1), ("pausa", 1)], tempo=120)   # le salva in un file
```

Le note si scrivono come `do4`, `fa#3`, `sib4` (il numero è l'ottava: `la4` = 440 Hz); `pausa` è il silenzio. `suono.durata_di("brano.wav")` dice quanto dura un file. Su Windows usa `winsound`, già incluso. I `.wav` si suonano subito; per mp3, ogg e gli altri formati serve ffmpeg (vedi sotto). Nella galleria di esempi trovi **Suoni e melodie**. Se esporti il progetto come Python, il file `suono.py` viene copiato accanto al programma.

## Il modulo `multimedia` (audio e video con ffmpeg)

`multimedia` usa **ffmpeg** per convertire, tagliare e guardare dentro i file audio e video. ffmpeg non è incluso in PitStudio: il modulo lo cerca da solo (nel PATH, nella variabile `PITONIT_FFMPEG` o nella cartella `.radfmpeg` della tua cartella utente). Se manca, scegli **Strumenti → ffmpeg: audio e video…**: la finestra ti dice cosa succede e, solo dopo il tuo consenso, lo scarica controllando l'impronta SHA-256 del file: puoi scegliere la versione essenziale (circa 115 MB) o quella completa (circa 200 MB, con più librerie). Dal programma: `multimedia.scarica_ffmpeg()`. Oppure installalo tu con `winget install ffmpeg`.

```pit sintassi
importa multimedia

dati = multimedia.info("film.mp4")                 # durata, formato, video e audio
stampa(dati["durata"], dati["video"][0]["larghezza"])

multimedia.converti("canzone.wav", "canzone.mp3")  # il formato lo decide l'estensione
# se il file di destinazione esiste già: errore, a meno di sovrascrivi=True
multimedia.estrai_audio("film.mp4", "colonna.mp3")
multimedia.taglia("film.mp4", "scena.mp4", inizio=10, fine=25)   # in secondi
multimedia.fotogramma("film.mp4", 12.5, "copertina.png")
multimedia.riduci("film.mp4", "piccolo.mp4", larghezza=640)

multimedia.converti("film.mp4", "film.gif", avanzamento=lambda frazione: stampa(f"{frazione:.0%}"))
```

Le funzioni che lavorano a lungo accettano `avanzamento`: una funzione che riceve un numero da 0 a 1. Se qualcosa non va ricevi un `ErroreMultimedia` con il motivo; se ffmpeg manca, un `FfmpegNonTrovato` che dice come procurarlo. Con ffmpeg `suono.riproduci("canzone.mp3")` suona anche mp3 e ogg (li converte al volo in un `.wav` temporaneo). Se esporti il progetto come Python, `multimedia.py` (e `suono.py`) vengono copiati accanto al programma.

`multimedia` è la scorciatoia per le cose semplici. Per **tutto** quello che ffmpeg sa fare (filtri, codec, più ingressi e uscite, avanzamento, cataloghi, ricette) c'è la libreria `ffmpeg`: vedi la pagina [ffmpeg: audio e video](#ffmpeg).

## Opzioni e valori in italiano

Per molte librerie anche le opzioni con nome sono tradotte, per esempio in tkinter:

```pit
importa interfaccia come tk

radice = tk.Finestra()
etichetta = tk.Etichetta(radice, testo="Ciao", sfondo="white")
etichetta.impacchetta(lato="sinistra", riempi="entrambi", espandi=Vero)
tk.Pulsante(radice, testo="Chiudi", comando=radice.distruggi).impacchetta()
radice.ciclo_principale()
```

## Metodi che la libreria richiama

Quando una libreria chiama un tuo metodo con un nome fisso, puoi usare il nome italiano:

| Libreria | Nome inglese | Nome italiano |
|---|---|---|
| unittest | `setUp`, `tearDown` | `prepara`, `smonta` |
| threading | `run` | `esegui` |
| http.server | `do_GET`, `do_POST` | `gestisci_GET`, `gestisci_POST` |
| html.parser | `handle_starttag`, `handle_data` | `gestisci_tag_iniziale`, `gestisci_dati` |
| json | `default` (nel codificatore) | `predefinito` |

## Librerie online e aggiornamenti

Le librerie nuove e le versioni più recenti si scaricano dal pannello **Librerie** (pulsanti **⟳ Novità**, **Installa / Aggiorna**): vedi la pagina «Aggiornamenti e librerie online».

## Elenco completo

{{librerie}}
