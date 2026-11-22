# Siti web e API con server_web

Il modulo **`server_web`** (incluso in pytonIta, niente da installare) è un **piccolo framework web**: pagine HTML, API in JSON con dati controllati, sessioni e accessi, modelli di pagina, file inviati con i moduli, documentazione automatica, e si può mettere dietro un server di produzione (WSGI/ASGI). Si impara passo per passo nelle lezioni [25](#lezione-25), [26](#lezione-26), [27](#lezione-27) e [28](#lezione-28); questa pagina è il riassunto per cercare qualcosa. Per usare **FastAPI** vero con i nomi italiani vedi [FastAPI in italiano](#fastapi).

## Un progetto pronto

*File → Nuovo progetto → Sito web o API (server)* crea un sito completo da guardare e cambiare: pagina, API di note con database SQLite, stili e script.

- **F5** accende il server. Nella console compare `Server in ascolto su http://127.0.0.1:8000/`: l'indirizzo è un **link**, un clic lo apre nel browser. Anche *Esegui → Apri il sito nel browser* apre l'ultimo indirizzo scritto dal programma.
- **Maiusc+F5** (Ferma) lo spegne. Per cambiare il codice, ferma e premi di nuovo F5.
- `/docs` mostra la documentazione automatica dell'API; nella galleria *Aiuto → Esempi* ci sono anche *Il mio primo sito* e *Libro degli ospiti*.

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
| `/utente/<nome>` o `/utente/{nome}` | pezzo variabile (testo) |
| `/articolo/<n:numero>` | intero (anche `<int:n>` o `{n}` con `n: tipo_intero`) |
| `/file/<percorso:resto>` | tutto il resto dell'indirizzo, barre comprese |
| `api = app.gruppo("/api")` | rotte con un prefisso comune: `@api.ottieni("/voci")` → `/api/voci` |
| `app.registra(gruppo, "/v2")` | collega un `Gruppo` creato a parte (per esempio in un altro file) |

## Parametri con tipo, modelli e 422

I parametri della funzione si **leggono e si controllano da soli** in base ai nomi e ai tipi:

- un nome che c'è nell'indirizzo (`<n>`) arriva dall'indirizzo;
- un parametro con un tipo di `Modello` (o chiamato `corpo`) arriva dal **corpo JSON**;
- gli altri arrivano dall'indirizzo come `?nome=valore` (con `list[tipo_intero]` si leggono i valori ripetuti: `?tag=1&tag=2`);
- `richiesta` è la richiesta intera; un valore predefinito rende il parametro facoltativo.

```pit sintassi
classe Voce(server_web.Modello):
    titolo: tipo_testo
    quantita: tipo_intero = 1
    tag: list[tipo_testo] = []


@app.rotta("/voci/<numero>")
definisci leggi(numero: tipo_intero, dettagli: bool = Falso):
    ritorna {"numero": numero, "dettagli": dettagli}


@app.invia("/voci")
definisci crea(voce: Voce):
    ritorna (voce.a_dizionario(), 201)
```

Se qualcosa non va, la risposta è **422** con l'elenco: `{"errori": [{"campo": "quantita", "dove": "corpo", "messaggio": "deve essere un numero intero"}]}`. I tipi ammessi sono testo, intero, decimale, `bool`, `list`, `list[tipo]`, `dict`, un altro `Modello` (anche annidato, anche in liste), e «o `Nessuno`» (`tipo_testo | Nessuno`). `Modello` si usa anche da solo: `Voce(titolo="pane")`, `Voce.da_dati({...})`, `voce.a_dizionario()`.

## Cosa ritornare

| Ritorni | Risposta |
|---|---|
| un testo | pagina HTML (200) |
| un dizionario, una lista o un `Modello` | JSON |
| byte | dati grezzi |
| `Nessuno` | vuota (204) |
| `(corpo, stato)` | con lo stato scelto, per esempio `("Creato", 201)` |
| `reindirizza("/altra")` | manda il browser a un'altra pagina (302) |
| `json_risposta(dati, stato)` | JSON con lo stato scelto |
| `Risposta(...)` | controllo totale: tipo, intestazioni, `imposta_cookie`, `togli_cookie` |

Per un errore: `solleva ErroreWeb(404, "messaggio")`. Un errore del programma dà **500** e il server **continua a funzionare**; l'errore completo compare nella console. Le funzioni possono essere `asincrono definisci`.

## Sessioni, accesso e CSRF

```pit sintassi
app.configura(chiave_segreta="un testo lungo e riservato", csrf=Vero)

@app.invia("/accedi")
definisci accedi(richiesta):
    se server_web.verifica_password(richiesta.form["password"], PASSWORD_CIFRATA):
        app.accedi(richiesta, "ada", ruoli=["admin"])
        ritorna reindirizza("/profilo")
    ritorna ("Credenziali sbagliate", 401)

@app.rotta("/profilo")
@app.richiede_accesso
definisci profilo(richiesta):
    ritorna {"utente": richiesta.utente}
```

- **`richiesta.sessione`** è un dizionario che il sito ricorda per ogni visitatore, in un **cookie firmato** (HttpOnly, SameSite, «Secure» su HTTPS): il visitatore non può modificarlo. Senza `chiave_segreta` la chiave è temporanea e le sessioni si perdono allo spegnimento. Tieni in sessione poche cose (l'identificativo dell'utente): il cookie ha un limite di circa 4 KB.
- **Password:** `cifra_password(testo)` produce un testo da salvare nel database (scrypt, con sale); `verifica_password(testo, cifrata)` controlla. Non si salva mai la password in chiaro.
- **Accesso:** `app.accedi(richiesta, utente, **dati)`, `app.esci(richiesta)`, `richiesta.utente`; `@app.richiede_accesso` manda chi non ha fatto l'accesso alla pagina `/accedi` (o risponde 401 per le API); `@app.richiede_accesso(ruolo="admin")` chiede anche il ruolo (403 altrimenti).
- **CSRF:** con `csrf=Vero` ogni POST/PUT/PATCH/DELETE deve rimandare il codice di `richiesta.token_csrf`: nei moduli HTML si mette `{{ campo_csrf }}`, nelle chiamate JSON l'intestazione `X-CSRF-Token`. Le rotte per altri programmi si escludono con `@app.senza_csrf`.
- **Intestazioni di sicurezza** (`X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`) sono aggiunte a ogni risposta; si cambiano con `configura(intestazioni_sicurezza=...)`.

## Modelli di pagina

`app.configura(cartella_pagine="pagine")` e poi `app.mostra("index.html", richiesta, titolo="...")`. Dentro la pagina:

| Si scrive | Cosa fa |
|---|---|
| `{{ nome }}` | il valore, **reso innocuo** (`< > & "` non diventano codice); manca = vuoto |
| `{{ utente.nome }}`, `{{ voci[0] }}` | attributi e indici |
| `{{ testo\|maiuscolo\|tronca(20) }}` | filtri: `grezzo`, `maiuscolo`, `minuscolo`, `titolo`, `lunghezza`, `json` (sicuro dentro `<script>`), `predefinito("n/d")`, `tronca(n)`, `data("%d/%m/%Y")`, `arrotonda(n)`, `ordina`, `inverti`, `unisci(", ")`, `primo`, `ultimo` |
| `{% se x > 2 e non finito %}…{% altrimenti_se … %}…{% altrimenti %}…{% fine %}` | condizioni (`e`, `o`, `non`, `in`, `Vero`, `Falso`, `Nessuno`) |
| `{% per voce in voci %}…{% altrimenti %}nessuna{% fine %}` | cicli; dentro c'è `ciclo.indice`, `ciclo.primo`, `ciclo.ultimo`, `ciclo.totale`; `per k, v in d.items()` |
| `{% estende "base.html" %}` e `{% blocco corpo %}…{% fine %}` | ereditarietà: la pagina base ha i blocchi, le altre li riempiono |
| `{% includi "menu.html" %}` | un pezzo di pagina |
| `{# commento #}` | non compare |

Con `richiesta` `mostra` aggiunge `richiesta`, `utente`, `csrf` e `campo_csrf`. Le espressioni sono **controllate**: niente chiamate arbitrarie, niente attributi che iniziano con `_` (un modello non può far eseguire codice). Fuori da `app.mostra`, `server_web.pagina(testo, nome=valore)` riempie un testo e `carica_pagina("file.html", …)` un file.

## File inviati

Un modulo con `enctype="multipart/form-data"` e `<input type="file" name="documento">`:

```pit sintassi
@app.invia("/carica")
definisci carica(richiesta):
    file_ricevuto = richiesta.file["documento"]
    percorso = file_ricevuto.salva("caricati")        # nome ripulito: non può uscire dalla cartella
    ritorna {"nome": file_ricevuto.nome_file, "byte": file_ricevuto.dimensione}
```

`richiesta.form` contiene anche i campi di testo dello stesso modulo. Il limite è 10 MB (`configura(dimensione_massima=...)`, 413 oltre).

## Documentazione automatica

`app.documentazione()` crea **`/docs`** (una pagina leggibile con indirizzi, parametri e corpi) e **`/openapi.json`** (la descrizione OpenAPI 3, da aprire con Swagger, Postman o per generare client). Tutto viene dai nomi, dai tipi, dai modelli e dalle docstring delle tue funzioni: la prima riga è il titolo, il resto la descrizione.

## Provare, avviare, metterlo in produzione

| Cosa | Come |
|---|---|
| provare una rotta **senza rete** | `app.simula("/saluta/Ada")`, con `"POST", json=...`, `form=...`, `file=...`, `cookie=...` → risposta con `stato`, `testo`, `dati`, `intestazioni` |
| provare un percorso intero (accesso, sessione, CSRF) | `c = app.cliente()` → `c.ottieni(...)`, `c.invia(...)`: ricorda i cookie; `c.sessione`, `c.imposta_sessione(...)`, `c.token_csrf` |
| accendere e restare in attesa | `app.avvia(porta=8000)` (con `apri_browser=Vero` apre anche il browser) |
| scegliere una porta libera | `porta=0` (l'indirizzo è scritto nella console) |
| accendere senza bloccare il programma | `server = app.avvia_in_sottofondo()` → `server.indirizzo`, `server.ferma()` |
| HTTPS | `app.avvia(certificato="cert.pem", chiave="chiave.pem")` (per provare: `mkcert` o `openssl`); i cookie diventano «Secure» |
| avvio e chiusura | `@app.all_avvio`, `@app.alla_chiusura` |
| prima e dopo ogni richiesta | `@app.prima_di_ogni_richiesta`, `@app.dopo_ogni_richiesta` |
| **WSGI** (waitress, gunicorn, mod_wsgi…) | l'applicazione stessa: `waitress.serve(app, port=8000)` |
| **ASGI** (uvicorn, hypercorn…) | `uvicorn.run(app.asgi)` |

Ogni richiesta scrive una riga nella console (`GET /pagina 200 (3 ms)`): si spegne con `Applicazione(registro=Falso)`.

## Sicurezza

- Il server integrato ascolta **solo su 127.0.0.1** (il tuo computer). `ascolta="0.0.0.0"` lo apre a tutta la rete: solo per provare.
- **Per un sito pubblico non usare `app.avvia`**: metti l'applicazione dietro un server di produzione (`waitress`, `gunicorn`, `uvicorn`), dietro un proxy con HTTPS (nginx, Caddy…), con `chiave_segreta` vera, `csrf=Vero`, `cookie_sicuro=Vero` e `DEBUG` spento. `server_web` non fa limiti di richieste, non protegge dagli attacchi di forza bruta sull'accesso, non gestisce utenti né permessi complessi: sono cose da aggiungere sopra (o da risolvere con un framework più grande: [FastAPI](#fastapi)).
- Il testo degli utenti non va mai messo in una pagina senza passare dai modelli (`{{ }}` lo rende innocuo); nell'SQL i valori vanno sempre con `?` (vedi la [lezione 26](#lezione-26)).

## Esportare in Python

I progetti con `server_web` si esportano come Python normale: il modulo viene copiato accanto al programma (come `suono`, `multimedia`, `ffmpeg` e `lettore`) e non serve altro. Per gli eseguibili («Crea l'eseguibile») valgono le stesse regole: chi riceve il programma non ha bisogno di nulla.
