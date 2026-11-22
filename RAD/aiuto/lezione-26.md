# Lezione 26 · Un sito con i dati

**Obiettivo:** costruire un sito che **salva** i dati in un database, riceve moduli e mette a disposizione un'**API** in JSON, senza aprire falle di sicurezza.

## Il progetto «Sito web o API»

*File → Nuovo progetto* e scegli il modello **Sito web o API (server)**. PitStudio crea:

| File | A cosa serve |
|---|---|
| `principale.pit` | le **rotte**: indirizzi, pagine e API |
| `pagine/index.html` | la pagina, con i **segnaposti** `{{ titolo }}` |
| `statici/stile.css`, `statici/app.js` | l'aspetto e lo script del browser |
| `note.db` | il database SQLite (si crea alla prima richiesta) |

Premi **F5**, clicca l'indirizzo nella console e prova a scrivere qualche nota. Il resto della lezione spiega come funziona, con esempi che si possono provare senza browser.

## Salvare i dati

Il database è quello della [lezione 20](#lezione-20): ogni rotta lo interroga. Questo è il «libro degli ospiti»: un modulo (`POST`) aggiunge un messaggio e rimanda alla pagina dell'elenco con `reindirizza`.

```pit
importa database
importa server_web

app = server_web.Applicazione(registro=Falso)
db = database.connetti(":memory:")
db.esegui("CREATE TABLE messaggi (id INTEGER PRIMARY KEY AUTOINCREMENT, autore TEXT, testo TEXT)")


@app.rotta("/messaggi", metodi=["GET", "POST"])
definisci messaggi(richiesta):
    se richiesta.metodo == "POST":
        autore = richiesta.valore("autore", "anonimo")
        contenuto = richiesta.valore("testo", "").strip()
        se non contenuto:
            ritorna server_web.json_risposta({"errore": "scrivi un messaggio"}, 400)
        db.esegui("INSERT INTO messaggi (autore, testo) VALUES (?, ?)", (autore, contenuto))
        db.conferma()
        ritorna server_web.reindirizza("/messaggi")
    righe = db.esegui("SELECT autore, testo FROM messaggi ORDER BY id").ottieni_tutti()
    ritorna [{"autore": chi, "testo": cosa} per chi, cosa in righe]


r = app.simula("/messaggi", "POST", form={"autore": "Ada", "testo": "Ciao!"})
stampa(r.stato, r.intestazioni["Location"])
app.simula("/messaggi", "POST", json={"autore": "Bruno", "testo": "Bella pagina"})
stampa(app.simula("/messaggi").dati)
stampa(app.simula("/messaggi", "POST", form={"testo": "  "}).stato)
```

```output
302 /messaggi
[{'autore': 'Ada', 'testo': 'Ciao!'}, {'autore': 'Bruno', 'testo': 'Bella pagina'}]
400
```

- `reindirizza("/messaggi")` risponde `302`: il browser va a quella pagina (così ricaricarla non rimanda il modulo);
- la stessa rotta serve sia un **modulo HTML** sia una chiamata **JSON**, perché `richiesta.valore` cerca nei due posti;
- una richiesta sbagliata riceve `400` con la spiegazione.

Nel modello, l'ultima versione apre il database a **ogni richiesta**: il server serve più persone insieme, e una connessione SQLite non si condivide tra più fili.

## Pagine con segnaposti

Un file HTML può avere dei **segnaposti**: `{{ nome }}` viene sostituito con un valore. `server_web.pagina(testo, nome=valore)` lavora su un testo; `server_web.carica_pagina("pagine/index.html", nome=valore)` legge prima il file.

```pit
importa server_web

modello = "<p>Ha scritto: {{ testo }}</p>"
stampa(server_web.pagina(modello, testo="Ciao & benvenuti"))
stampa(server_web.pagina(modello, testo="<script>alert(1)</script>"))
stampa(server_web.pagina("<div>{{ html|grezzo }}</div>", html="<b>grassetto</b>"))
```

```output
<p>Ha scritto: Ciao &amp; benvenuti</p>
<p>Ha scritto: &lt;script&gt;alert(1)&lt;/script&gt;</p>
<div><b>grassetto</b></div>
```

I caratteri speciali (`<`, `>`, `&`, `"`) vengono **resi innocui**: se un visitatore scrive uno script nel tuo libro degli ospiti, il browser lo mostra come testo invece di eseguirlo. Il filtro `|grezzo` lo disattiva: usalo **solo per HTML scritto da te**, mai per ciò che arriva dagli utenti.

## Sicurezza: due regole d'oro

1. **Mai fidarsi di ciò che arriva dal browser.** Controlla che i campi ci siano e abbiano senso (come fa la rotta con `400`), e non mettere testo degli utenti in una pagina senza `pagina()`/`textContent`.
2. **Valori nell'SQL sempre con `?`.** Mettere il testo dell'utente dentro la stringa SQL permette di cambiare la domanda al database:

```pit
importa database

db = database.connetti(":memory:")
db.esegui("CREATE TABLE utenti (nome TEXT)")
db.esegui_molti("INSERT INTO utenti VALUES (?)", [("Ada",), ("Bruno",)])
cercato = "x' OR '1'='1"
sbagliato = db.esegui("SELECT nome FROM utenti WHERE nome = '" + cercato + "'").ottieni_tutti()
giusto = db.esegui("SELECT nome FROM utenti WHERE nome = ?", (cercato,)).ottieni_tutti()
stampa(lunghezza_di(sbagliato), lunghezza_di(giusto))
```

```output
2 0
```

Con la stringa «incollata» il visitatore ha ottenuto **tutte** le righe; con il `?` il testo resta un valore e non trova nulla.

## Cookie e file statici

Un **cookie** è un piccolo dato che il browser conserva e rimanda a ogni richiesta (per esempio per riconoscerti). Si legge con `richiesta.cookie` e si imposta con `Risposta.imposta_cookie`.

```pit
importa server_web

app = server_web.Applicazione(registro=Falso)


@app.rotta("/visite")
definisci visite(richiesta):
    numero = tipo_intero(richiesta.cookie.get("visite", "0")) + 1
    risposta = server_web.Risposta({"visite": numero})
    risposta.imposta_cookie("visite", tipo_testo(numero))
    ritorna risposta


stampa(app.simula("/visite").dati)
stampa(app.simula("/visite", cookie={"visite": "4"}).dati)
```

```output
{'visite': 1}
{'visite': 5}
```

I **file statici** (stili, immagini, script) si servono con `app.statici("/statici", "cartella")`: tutto ciò che sta nella cartella diventa raggiungibile sotto quell'indirizzo, ma **solo** quella cartella (i percorsi con `..` sono rifiutati).

## Il sito è tuo: cosa aggiungere

- più pagine: una rotta e un file in `pagine/` per ciascuna;
- un archivio più grande: una tabella in più e le rotte per leggerla;
- l'aspetto: modifica `statici/stile.css` e ricarica la pagina (non serve riavviare il server per i file statici; per il codice sì: **F5** di nuovo).

## Esercizi

1. Una rotta `/spesa` che con `POST` (JSON `{"voce": "pane"}`) aggiunge una voce a una lista e con `GET` ritorna la lista. Provala con `simula`.
2. Un contatore di visite con un cookie, come nell'esempio, ma che ricominci da 1 se il cookie non è un numero (consiglio: `isdigit()`).
3. Una rotta `/cerca?q=ca` che ritorna le parole di una lista che **contengono** il testo cercato.

## Soluzioni

```pit
importa server_web

app = server_web.Applicazione(registro=Falso)
spesa = []


@app.rotta("/spesa", metodi=["GET", "POST"])
definisci voci_spesa(richiesta):
    se richiesta.metodo == "POST":
        spesa.append(richiesta.json["voce"])
        ritorna ({"totale": lunghezza_di(spesa)}, 201)
    ritorna spesa


app.simula("/spesa", "POST", json={"voce": "pane"})
app.simula("/spesa", "POST", json={"voce": "latte"})
stampa(app.simula("/spesa").dati)
```

```output
['pane', 'latte']
```

```pit
importa server_web

app = server_web.Applicazione(registro=Falso)


@app.rotta("/visite")
definisci visite(richiesta):
    valore = richiesta.cookie.get("visite", "0")
    numero = (tipo_intero(valore) se valore.isdigit() altrimenti 0) + 1
    risposta = server_web.Risposta({"visite": numero})
    risposta.imposta_cookie("visite", tipo_testo(numero))
    ritorna risposta


stampa(app.simula("/visite", cookie={"visite": "abc"}).dati)
stampa(app.simula("/visite", cookie={"visite": "9"}).dati)
```

```output
{'visite': 1}
{'visite': 10}
```

```pit
importa server_web

app = server_web.Applicazione(registro=Falso)
PAROLE = ["casa", "cane", "gatto", "cena"]


@app.rotta("/cerca")
definisci cerca(richiesta):
    cercato = richiesta.parametri.get("q", "").lower()
    ritorna [p per p in PAROLE se cercato in p]


stampa(app.simula("/cerca?q=ca").dati)
```

```output
['casa', 'cane']
```
