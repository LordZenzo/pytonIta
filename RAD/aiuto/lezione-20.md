# Lezione 20 · I database con SQLite

**Obiettivo:** salvare dati in **tabelle** e interrogarli con poche righe di SQL, senza installare nulla.

## Perché un database

Un file di testo va bene per poche righe. Quando i dati sono tanti, devi cercarli, ordinarli e correggerli senza riscrivere tutto, serve un **database**. **SQLite** è un database contenuto in un solo file (di solito con estensione `.db`) e Python lo include: nessun server da installare.

Un database è fatto di **tabelle**, come fogli di calcolo: ogni **colonna** ha un nome e un tipo, ogni **riga** è un record.

| id | nome | voto |
|---|---|---|
| 1 | Anna | 9 |
| 2 | Luca | 7 |

Il modulo si chiama `database` (in inglese `sqlite3`).

## Connettersi e creare una tabella

```pit
importa database

db = database.connetti(":memory:")
db.esegui("CREATE TABLE studenti (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, voto INTEGER)")
db.conferma()
stampa("tabella creata")
db.chiudi()
```

```output
tabella creata
```

- `connetti("scuola.db")` apre (o crea) il file; `":memory:"` crea un database **temporaneo** in memoria, perfetto per provare;
- `esegui(...)` manda un comando **SQL**;
- `conferma()` rende definitive le modifiche, `chiudi()` chiude il collegamento.

I comandi SQL più importanti sono quattro:

| Comando | Fa |
|---|---|
| `INSERT INTO` | aggiunge una riga |
| `SELECT` | legge righe |
| `UPDATE` | cambia righe esistenti |
| `DELETE` | toglie righe |

## Inserire i dati: mai con le f-string!

I valori variabili si passano con i **segnaposto** `?` e una tupla. Non incollare mai i valori dentro il testo SQL: sarebbe una porta aperta alla *SQL injection* (qualcuno scrive nel campo nome un comando che cancella tutto).

```pit
importa database

db = database.connetti(":memory:")
db.esegui("CREATE TABLE studenti (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, voto INTEGER)")
db.esegui("INSERT INTO studenti (nome, voto) VALUES (?, ?)", ("Anna", 9))
db.esegui_molti("INSERT INTO studenti (nome, voto) VALUES (?, ?)", [("Luca", 7), ("Sara", 8)])
db.conferma()
stampa(db.esegui("SELECT COUNT(*) FROM studenti").ottieni_uno())
db.chiudi()
```

```output
(3,)
```

`esegui_molti` ripete lo stesso comando per tante righe in un colpo solo.

## Leggere i dati

`SELECT` restituisce un cursore; `ottieni_tutti()` dà tutte le righe (ognuna è una tupla) e `ottieni_uno()` solo la prima:

```pit
importa database

db = database.connetti(":memory:")
db.esegui("CREATE TABLE studenti (nome TEXT, voto INTEGER)")
db.esegui_molti("INSERT INTO studenti VALUES (?, ?)", [("Anna", 9), ("Luca", 7), ("Sara", 8)])

cursore = db.esegui("SELECT nome, voto FROM studenti ORDER BY voto DESC")
per riga in cursore.ottieni_tutti():
    stampa(riga)

stampa(db.esegui("SELECT AVG(voto) FROM studenti").ottieni_uno())
db.chiudi()
```

```output
('Anna', 9)
('Sara', 8)
('Luca', 7)
(8.0,)
```

- `ORDER BY voto DESC` ordina dal voto più alto;
- `AVG`, `COUNT`, `SUM`, `MIN`, `MAX` calcolano al volo la media, il numero, la somma, il minimo e il massimo.

Si filtra con `WHERE`:

```pit
importa database

db = database.connetti(":memory:")
db.esegui("CREATE TABLE studenti (nome TEXT, voto INTEGER)")
db.esegui_molti("INSERT INTO studenti VALUES (?, ?)", [("Anna", 9), ("Luca", 7), ("Sara", 8)])

soglia = 8
per nome, voto in db.esegui("SELECT nome, voto FROM studenti WHERE voto >= ?", (soglia,)):
    stampa(nome, voto)
db.chiudi()
```

```output
Anna 9
Sara 8
```

## Correggere e cancellare

```pit
importa database

db = database.connetti(":memory:")
db.esegui("CREATE TABLE studenti (nome TEXT, voto INTEGER)")
db.esegui_molti("INSERT INTO studenti VALUES (?, ?)", [("Anna", 9), ("Luca", 7)])

db.esegui("UPDATE studenti SET voto = ? WHERE nome = ?", (8, "Luca"))
db.esegui("DELETE FROM studenti WHERE nome = ?", ("Anna",))
db.conferma()
stampa(db.esegui("SELECT * FROM studenti").ottieni_tutti())
db.chiudi()
```

```output
[('Luca', 8)]
```

> Dimenticare `WHERE` in un `UPDATE` o `DELETE` cambia o cancella **tutte** le righe. Controlla sempre la condizione.

## Chiudere sempre, con `con`

Il blocco `con` conferma da solo se tutto va bene e annulla se c'è un errore:

```pit
importa database

con database.connetti(":memory:") come db:
    db.esegui("CREATE TABLE note (testo TEXT)")
    db.esegui("INSERT INTO note VALUES (?)", ("comprare il pane",))
    stampa(db.esegui("SELECT testo FROM note").ottieni_uno()[0])
```

```output
comprare il pane
```

## Con PitStudio

Non devi scrivere SQL a mano per forza: in PitStudio il menu **Database** apre un gestore con le tabelle, i dati che si correggono con un doppio clic, la creazione guidata di tabelle e un editor SQL. Un file `.db` si apre con un doppio clic nel pannello del progetto. La guida spiega anche come costruire una **maschera** (una finestra collegata a una tabella) dalla [pagina dei database](#database).

## Esercizi

1. Crea una tabella `libri (titolo, anno)`, inserisci tre libri e stampa quelli usciti **dopo il 2000**.
2. Aggiungi alla tabella della lezione una colonna `città` nella `CREATE TABLE`, inserisci due righe e stampa quante sono per ogni città (usa `GROUP BY`).
3. Scrivi una funzione `aggiungi_studente(db, nome, voto)` che inserisce una riga, e una `media_voti(db)` che restituisce la media. Provale.

## Soluzioni

```pit
importa database

db = database.connetti(":memory:")
db.esegui("CREATE TABLE libri (titolo TEXT, anno INTEGER)")
db.esegui_molti("INSERT INTO libri VALUES (?, ?)", [("Il nome della rosa", 1980), ("Gomorra", 2006), ("L'amica geniale", 2011)])
per riga in db.esegui("SELECT titolo FROM libri WHERE anno > 2000 ORDER BY anno"):
    stampa(riga[0])
db.chiudi()
```

```output
Gomorra
L'amica geniale
```

```pit
importa database

db = database.connetti(":memory:")
db.esegui("CREATE TABLE studenti (nome TEXT, citta TEXT)")
db.esegui_molti("INSERT INTO studenti VALUES (?, ?)", [("Anna", "Roma"), ("Luca", "Roma"), ("Sara", "Milano")])
per citta, quanti in db.esegui("SELECT citta, COUNT(*) FROM studenti GROUP BY citta ORDER BY citta"):
    stampa(citta, quanti)
db.chiudi()
```

```output
Milano 1
Roma 2
```

```pit
importa database

definisci aggiungi_studente(db, nome, voto):
    db.esegui("INSERT INTO studenti (nome, voto) VALUES (?, ?)", (nome, voto))
    db.conferma()

definisci media_voti(db):
    ritorna db.esegui("SELECT AVG(voto) FROM studenti").ottieni_uno()[0]

db = database.connetti(":memory:")
db.esegui("CREATE TABLE studenti (nome TEXT, voto INTEGER)")
aggiungi_studente(db, "Anna", 9)
aggiungi_studente(db, "Luca", 7)
stampa(media_voti(db))
db.chiudi()
```

```output
8.0
```
