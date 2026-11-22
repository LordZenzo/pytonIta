# Lezione 25 · Il web: il tuo primo server

**Obiettivo:** creare con poche righe un **server web**: un programma che risponde alle richieste di un browser con pagine e dati.

## Che cos'è un server web

Quando scrivi un indirizzo nel browser, questo manda una **richiesta** a un altro computer; quel computer, il **server**, manda indietro una **risposta** (una pagina, un'immagine, dei dati). Un server web è un programma sempre in attesa di richieste.

L'indirizzo ha tre pezzi che ti serviranno:

| Pezzo | Esempio | Cosa dice |
|---|---|---|
| computer | `127.0.0.1` | `127.0.0.1` è **il tuo stesso computer**: nessun altro lo vede |
| porta | `8000` | la «porta» a cui il server è in ascolto (ce ne sono tante per volta) |
| percorso | `/saluta/Ada` | quale pagina vuoi: il server decide cosa rispondere |

Ogni risposta ha anche un **stato**, un numero: `200` è «tutto bene», `404` «non esiste», `405` «questo metodo non vale qui», `500` «il programma ha sbagliato».

Il modulo che usiamo si chiama `server_web` ed è incluso in pytonIta: niente da installare.

## Il primo server

```pit sintassi
importa server_web

app = server_web.Applicazione()


@app.rotta("/")
definisci home():
    ritorna "<h1>Ciao dal mio server!</h1>"


app.avvia(porta=8000)
```

Se provi questo programma (**F5**), nella console compare `Server in ascolto su http://127.0.0.1:8000/`: **clicca l'indirizzo** (oppure *Esegui → Apri il sito nel browser*) e vedrai la tua pagina. Per spegnerlo premi **Maiusc+F5** (Ferma).

- `Applicazione()` è il tuo sito;
- `@app.rotta("/")` collega un **indirizzo** a una **funzione**: quando il browser chiede `/`, parte `home()`;
- ciò che la funzione `ritorna` è la risposta;
- `avvia()` accende il server e resta lì ad aspettare.

Per esercitarti puoi anche creare un progetto con il modello **Sito web o API** (*File → Nuovo progetto*): contiene già un sito completo da guardare e modificare.

## Rotte e risposte

Cosa ritorni decide che tipo di risposta arriva al browser:

| Ritorni | Il browser riceve |
|---|---|
| un testo | una pagina HTML |
| un dizionario o una lista | dati **JSON** (il formato con cui i programmi si scambiano i dati) |
| `Nessuno` | una risposta vuota (204) |
| `(corpo, stato)` | il corpo con lo stato che scegli, per esempio `("Creato", 201)` |

Per provare le rotte **senza accendere il server** c'è `app.simula(indirizzo)`: ritorna la risposta, con `stato`, `testo` e (per le API) `dati`.

```pit
importa server_web

app = server_web.Applicazione(registro=Falso)


@app.rotta("/")
definisci home():
    ritorna "<h1>Ciao dal mio server!</h1>"


@app.rotta("/ora")
definisci ora():
    ritorna {"ore": 12, "minuti": 30}


risposta = app.simula("/")
stampa(risposta.stato)
stampa(risposta.testo)
stampa(app.simula("/ora").dati)
```

```output
200
<h1>Ciao dal mio server!</h1>
{'ore': 12, 'minuti': 30}
```

(`registro=Falso` spegne le righe che il server scrive per ogni richiesta, utili quando lo accendi davvero.)

## Pezzi variabili nell'indirizzo

Tra `<` e `>` si scrive un **pezzo variabile**: la parte dell'indirizzo che cambia diventa un parametro della funzione.

- `<nome>` è un testo;
- `<n:numero>` è un **numero intero** (se l'indirizzo non ha un numero, la rotta non corrisponde);
- `<percorso:resto>` prende anche le barre (`/file/a/b/c.txt`).

```pit
importa server_web

app = server_web.Applicazione(registro=Falso)


@app.rotta("/saluta/<nome>")
definisci saluta(nome):
    ritorna {"messaggio": "Ciao " + nome + "!"}


@app.rotta("/somma/<a:numero>/<b:numero>")
definisci somma(a, b):
    ritorna {"risultato": a + b}


stampa(app.simula("/saluta/Ada").dati)
stampa(app.simula("/somma/2/40").dati)
stampa(app.simula("/somma/due/40").stato)
```

```output
{'messaggio': 'Ciao Ada!'}
{'risultato': 42}
404
```

## Errori e stati

Per rispondere con un errore si **solleva** `ErroreWeb(stato, messaggio)`; per scegliere lo stato di una risposta normale si ritorna una coppia. Il server non si ferma mai per un errore del programma: risponde `500` e continua (l'errore compare nella console, così lo correggi).

```pit
importa server_web

app = server_web.Applicazione(registro=Falso)
UTENTI = {1: "Ada", 2: "Bruno"}


@app.rotta("/utente/<numero:numero>")
definisci utente(numero):
    se numero non in UTENTI:
        solleva server_web.ErroreWeb(404, "Utente sconosciuto")
    ritorna {"nome": UTENTI[numero]}


@app.errore(404)
definisci non_trovato():
    ritorna "<h1>Qui non c'è nulla</h1>"


stampa(app.simula("/utente/1").dati)
r = app.simula("/utente/7")
stampa(r.stato, r.testo)
```

```output
{'nome': 'Ada'}
404 <h1>Qui non c'è nulla</h1>
```

`@app.errore(404)` sostituisce la pagina di errore predefinita con la tua.

## Moduli e JSON

Di solito una rotta risponde solo a **GET** (leggere). Per ricevere dati si usa **POST**: `@app.invia("/iscrivi")`. La funzione che chiede `richiesta` trova i dati inviati:

- `richiesta.form`: i campi di un **modulo HTML** (`<form method="post">`);
- `richiesta.json`: i dati JSON mandati da uno script;
- `richiesta.parametri`: quelli nell'indirizzo (`/cerca?q=casa`);
- `richiesta.valore("nome")`: li cerca nei tre posti.

```pit
importa server_web

app = server_web.Applicazione(registro=Falso)


@app.invia("/iscrivi")
definisci iscrivi(richiesta):
    nome = richiesta.form.get("nome", "").strip()
    se non nome:
        ritorna server_web.json_risposta({"errore": "manca il nome"}, 400)
    ritorna ({"iscritto": nome}, 201)


r = app.simula("/iscrivi", "POST", form={"nome": "Ada"})
stampa(r.stato, r.dati)
r = app.simula("/iscrivi", "POST", form={})
stampa(r.stato, r.dati)
stampa(app.simula("/iscrivi").stato)
```

```output
201 {'iscritto': 'Ada'}
400 {'errore': 'manca il nome'}
405
```

L'ultima riga mostra il **405**: l'indirizzo esiste ma solo per POST.

## Provare senza browser

`app.simula(...)` è il modo più comodo per **controllare il sito con dei test**, anche automatici (vedi la [lezione sui test](#lezione-21)): si scrive quello che ci aspettiamo e si verifica.

```pit
importa server_web

app = server_web.Applicazione(registro=Falso)


@app.rotta("/doppio/<n:numero>")
definisci doppio(n):
    ritorna {"doppio": n * 2}


asserisci app.simula("/doppio/21").dati == {"doppio": 42}
asserisci app.simula("/doppio/x").stato == 404
stampa("il sito funziona")
```

```output
il sito funziona
```

## Attenzione: chi può vederlo

- `avvia()` ascolta solo su `127.0.0.1`: **solo tu** puoi aprire il sito. È la scelta giusta mentre impari.
- Con `avvia(ascolta="0.0.0.0")` lo vedono tutti i computer della tua rete: fallo solo per provare, mai con dati riservati.
- Questo server è fatto per imparare e per piccoli strumenti. Per un sito aperto al pubblico servono un servizio di hosting e un server pensato per Internet (e molte attenzioni alla sicurezza).

## Esercizi

1. Scrivi la rotta `/raddoppia/<n:numero>` che ritorna `{"risultato": ...}` con il doppio di `n`. Provala con `simula`.
2. Scrivi la rotta `/benvenuto/<nome>` che ritorna `<h1>Benvenuto, NOME!</h1>`, usando `server_web.pagina` così che un nome come `<b>x` non diventi codice HTML.
3. Metti una pagina tua per l'errore 404 e controlla che `simula("/boh")` dia stato 404 con il tuo testo.

## Soluzioni

```pit
importa server_web

app = server_web.Applicazione(registro=Falso)


@app.rotta("/raddoppia/<n:numero>")
definisci raddoppia(n):
    ritorna {"risultato": n * 2}


stampa(app.simula("/raddoppia/21").dati)
```

```output
{'risultato': 42}
```

```pit
importa server_web

app = server_web.Applicazione(registro=Falso)


@app.rotta("/benvenuto/<nome>")
definisci benvenuto(nome):
    ritorna server_web.pagina("<h1>Benvenuto, {{ nome }}!</h1>", nome=nome)


stampa(app.simula("/benvenuto/Ada").testo)
stampa(app.simula("/benvenuto/%3Cb%3Ex").testo)
```

```output
<h1>Benvenuto, Ada!</h1>
<h1>Benvenuto, &lt;b&gt;x!</h1>
```

```pit
importa server_web

app = server_web.Applicazione(registro=Falso)


@app.errore(404)
definisci non_trovato():
    ritorna "<h1>Qui non c'è nulla</h1>"


r = app.simula("/boh")
stampa(r.stato, r.testo)
```

```output
404 <h1>Qui non c'è nulla</h1>
```
