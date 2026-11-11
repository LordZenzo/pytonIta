## Questo progetto usa pytonIta (PitStudio)

Lingua: **rispondi in italiano**, in modo breve e concreto. I programmi di questo progetto sono file **`.pit`**: Python con parole chiave italiane,
eseguito dall'interprete **pitonit** (un CPython vero, senza traduzione intermedia). I file `.py` restano Python normale (parole inglesi).

### Come si eseguono e si provano
- Eseguire: `"{{pitonit}}" file.pit`  (con argomenti: `"{{pitonit}}" file.pit arg1 arg2`)
- Controllare la sintassi senza eseguire: `"{{pitonit}}" -c "compile(open('file.pit', encoding='utf-8').read(), 'file.pit', 'exec', 0x10000, True)"`
- I nomi italiani delle librerie: `"{{pitonit}}" -c "importa matematica; stampa([n per n in elenca(matematica) se non n.startswith('_')])"`
- PitStudio controlla da solo la sintassi di ogni `.pit`/`.py` dopo ogni scrittura: se ricevi un errore di sintassi, correggilo subito.

### Regole del linguaggio (nei `.pit` le parole chiave inglesi non esistono)
| inglese | italiano | inglese | italiano |
|---|---|---|---|
| if / elif / else | se / altrimenti_se / altrimenti | for … in / while | per … in / mentre |
| def / return / class | definisci / ritorna / classe | import / from / as | importa / da / come |
| try / except / finally / raise | prova / eccetto / infine / solleva | with / pass | con / passa |
| and / or / not | e / o / non | is / is not | è / è non |
| break / continue / yield | interrompi / continua / produci | global / del / lambda | globale / elimina / lambda |
| async / await / assert | asincrono / attendi / asserisci | True / False / None | Vero / Falso / Nessuno |

- `x if c else y` si scrive `x se c altrimenti y`; `self` per convenzione è `se_stesso`; `__init__` è `__inizializza__`, `__str__` è `__testo__`.
- Funzioni predefinite in italiano: `stampa`, `leggi` (input), `lunghezza`, `intervallo`, `intero`, `decimale`, `testo`, `lista`, `dizionario`, `insieme`,
  `somma`, `massimo`, `minimo`, `ordinato`, `enumera`, `abbina`, `apri`, `tipo`, `arrotonda`. Metodi: `lista.aggiungi/estrai/ordina`, `testo.separa/unisci/maiuscolo/sostituisci`,
  `dizionario.chiavi/valori/elementi/ottieni`. I nomi inglesi continuano a funzionare.
- Opzioni anche in italiano: `ordinato_di(x, chiave=f, inverso=Vero)`, `massimo_di(x, predefinito=0)`, `apri(nome, modalita="w", codifica="utf-8")`, `stampa(a, b, separatore="-", fine="")`.
- `True`, `False`, `None` nei `.pit` sono un errore: usa `Vero`, `Falso`, `Nessuno`.
- Parole come `classe`, `con`, `da`, `prova` sono accettate come nomi di variabile dove non c'è ambiguità, ma a inizio istruzione sono parole chiave: preferisci nomi diversi.
- `elimina(x)` attaccato alla parentesi è una chiamata di funzione; `elimina x` cancella il nome.
- Librerie con nomi italiani: `matematica`, `casuale`, `tempo`, `data_ora`, `sistema`, `sistema_operativo`, `percorso`, `formato_json`, `tabelle_csv`, `espressioni_regolari`,
  `collezioni`, `database` (sqlite3), `interfaccia` (tkinter), `richieste`, `statistica`… I nomi originali (`math`, `json`, `tkinter`) funzionano sempre: nel dubbio usali.

### Come lavorare
- Prima di scrivere guarda i file esistenti; fai modifiche piccole e mirate (PitStudio le fotografa: l'utente può annullare l'ultima richiesta dal pulsante «Annulla»).
- Non toccare le cartelle `.rad` e `.claude`. I file `*_ui.pit` sono generati dal progettista di finestre di PitStudio: non modificarli a mano.
- Dopo aver scritto codice, eseguilo (o esegui i test) e riferisci l'esito.
