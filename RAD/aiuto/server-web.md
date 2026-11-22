# Siti web e API con server_web

Il modulo **`server_web`** (incluso in pytonIta, niente da installare) crea un **server web**: pagine HTML, API in JSON, moduli e file statici, con poche righe e tutto in italiano. Si impara passo per passo nelle [lezioni 25 e 26](#lezione-25); questa pagina è il riassunto per chi vuole solo cercare qualcosa.

## Un progetto pronto

*File → Nuovo progetto → Sito web o API (server)* crea un sito completo da guardare e cambiare: pagina, API di note con database SQLite, stili e script.

- **F5** accende il server. Nella console compare `Server in ascolto su http://127.0.0.1:8000/`: l'indirizzo è un **link**, un clic lo apre nel browser. Anche *Esegui → Apri il sito nel browser* apre l'ultimo indirizzo scritto dal programma.
- **Maiusc+F5** (Ferma) lo spegne. Per cambiare il codice, ferma e premi di nuovo F5.
- Nella galleria *Aiuto → Esempi* ci sono anche *Il mio primo sito* e *Libro degli ospiti* (categoria «Web»).

## Il minimo

```pit sintassi
importa server_web

app = server_web.Applicazione()


@app.rotta("/")
definisci home():
    ritorna "<h1>Ciao!</h1>"


@app.rotta("/saluta/<nome>")
definisci saluta(nome):
    ritorna {"messaggio": "Ciao " + nome}


app.avvia(porta=8000)
```

## Le rotte

| Si scrive | Significa |
|---|---|
| `@app.rotta("/percorso")` | risponde a **GET** |
| `@app.rotta("/percorso", metodi=["GET", "POST"])` | più metodi |
| `@app.invia("/percorso")` | solo **POST** (moduli, dati inviati) |
| `@app.modifica(...)`, `@app.elimina_rotta(...)` | PUT/PATCH, DELETE |
| `/utente/<nome>` | pezzo variabile (testo) |
| `/articolo/<n:numero>` | intero (anche `<int:n>` alla maniera di Flask) |
| `/file/<percorso:resto>` | tutto il resto dell'indirizzo, barre comprese |

La funzione può chiedere un parametro **`richiesta`** (metodo, percorso, `parametri`, `form`, `json`, `cookie`, `intestazioni`, `testo`, `valore("nome")`) e i pezzi variabili.

## Cosa ritornare

| Ritorni | Risposta |
|---|---|
| un testo | pagina HTML (200) |
| un dizionario o una lista | JSON |
| byte | dati grezzi |
| `Nessuno` | vuota (204) |
| `(corpo, stato)` | con lo stato scelto, per esempio `("Creato", 201)` |
| `reindirizza("/altra")` | manda il browser a un'altra pagina (302) |
| `json_risposta(dati, stato)` | JSON con lo stato scelto |
| `Risposta(...)` | controllo totale: tipo, intestazioni, `imposta_cookie`, `togli_cookie` |

Per un errore: `solleva ErroreWeb(404, "messaggio")`. Un errore del programma dà **500** (con il messaggio per chi sviluppa) e il server **continua a funzionare**; l'errore completo compare nella console.

## Pagine e file

- `pagina(testo, nome=valore)` e `carica_pagina("pagine/index.html", nome=valore)` sostituiscono i segnaposti `{{ nome }}`. I caratteri speciali sono resi innocui; `{{ nome|grezzo }}` li lascia come sono (solo per HTML scritto da te).
- `app.statici("/statici", "cartella")` serve i file di una cartella (e solo quella: `..` è rifiutato).
- `@app.errore(404)` personalizza la pagina di un errore; `@app.prima_di_ogni_richiesta` esegue un controllo prima di ogni rotta (se ritorna qualcosa, quella è la risposta).
- `app.dati` è un dizionario dove tenere ciò che serve a più rotte.

## Avviare, provare, spegnere

| Cosa | Come |
|---|---|
| accendere e restare in attesa | `app.avvia(porta=8000)` (con `apri_browser=Vero` apre anche il browser) |
| scegliere una porta libera | `porta=0` (l'indirizzo è scritto nella console) |
| accendere senza bloccare il programma | `server = app.avvia_in_sottofondo()` → `server.indirizzo`, `server.ferma()` (utile con una finestra tkinter) |
| provare una rotta **senza rete** | `app.simula("/saluta/Ada")`, con `"POST", json=...`, `form=...`, `cookie=...` → risposta con `stato`, `testo`, `dati`, `intestazioni` |

Ogni richiesta scrive una riga nella console (`GET /pagina 200 (3 ms)`): si spegne con `Applicazione(registro=Falso)`.

## Sicurezza

- Il server ascolta **solo su 127.0.0.1** (il tuo computer). `ascolta="0.0.0.0"` lo apre a tutta la rete: solo per provare, mai con dati riservati.
- Non è un server per il pubblico di Internet: per quello servono un hosting e un server di produzione.
- Il testo degli utenti non va mai messo in una pagina senza `pagina()`; nell'SQL i valori vanno sempre con `?` (vedi la [lezione 26](#lezione-26)).
- Le richieste sopra i 10 MB sono rifiutate (413).

## Esportare in Python

I progetti con `server_web` si esportano come Python normale: il modulo viene copiato accanto al programma (come `suono`, `multimedia`, `ffmpeg` e `lettore`) e non serve altro.
