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
