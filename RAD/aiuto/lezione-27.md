# Lezione 27 · Un'API come i professionisti

**Obiettivo:** far controllare i dati al server (tipi, modelli, errori 422) e farsi scrivere la documentazione, come fanno i framework professionali.

## Perché controllare i dati

Chi chiama la tua API può mandare **qualsiasi cosa**: un numero dove aspetti un testo, un campo che manca, una lista invece di un oggetto. Se controlli a mano ogni cosa, il codice si riempie di `se`. `server_web` lo fa per te, in base ai **tipi** che scrivi accanto ai parametri, come in FastAPI. Se i dati non vanno, il browser riceve **422** con l'elenco di cosa non va; la tua funzione parte solo quando tutto è a posto.

## Parametri con tipo

I parametri della funzione vengono cercati per nome: nell'indirizzo se c'è un pezzo `<nome>`, altrimenti nella parte dopo il `?`. Il tipo li converte; il valore predefinito li rende facoltativi.

```pit
importa server_web

app = server_web.Applicazione(registro=Falso)


@app.rotta("/prodotti/<codice>")
definisci prodotto(codice: tipo_intero, sconto: tipo_decimale = 0.0):
    ritorna {"codice": codice, "sconto": sconto}


stampa(app.simula("/prodotti/12?sconto=0.5").dati)
r = app.simula("/prodotti/abc")
stampa(r.stato)
stampa(r.dati["errori"][0]["campo"], r.dati["errori"][0]["dove"])
```

```output
{'codice': 12, 'sconto': 0.5}
422
codice indirizzo
```

I tipi che si possono usare: `tipo_testo`, `tipo_intero`, `tipo_decimale`, `bool` (accetta `true`, `si`, `1`…), `list[tipo_intero]` (per `?tag=1&tag=2`), e i modelli della prossima sezione.

## Modelli di dati

Per i dati che arrivano nel **corpo** della richiesta (di solito JSON) si descrive la loro forma con un `Modello`: una classe con i campi e il loro tipo.

```pit
importa server_web

app = server_web.Applicazione(registro=Falso)


classe Prodotto(server_web.Modello):
    nome: tipo_testo
    prezzo: tipo_decimale
    disponibile: bool = Vero


@app.invia("/prodotti")
definisci nuovo(prodotto: Prodotto):
    ritorna ({"nome": prodotto.nome, "prezzo": prodotto.prezzo, "disponibile": prodotto.disponibile}, 201)


r = app.simula("/prodotti", "POST", json={"nome": "Penna", "prezzo": 1.5})
stampa(r.stato, r.dati)
r = app.simula("/prodotti", "POST", json={"nome": "Penna", "prezzo": "tanto"})
stampa(r.stato, r.dati["errori"])
r = app.simula("/prodotti", "POST", json={"prezzo": 2})
stampa(r.stato, [voce["campo"] per voce in r.dati["errori"]])
```

```output
201 {'nome': 'Penna', 'prezzo': 1.5, 'disponibile': Vero}
422 [{'campo': 'prezzo', 'dove': 'corpo', 'messaggio': 'deve essere un numero'}]
422 ['nome']
```

- il **parametro con il tipo del modello** (`prodotto: Prodotto`) riceve il JSON già controllato: nome e prezzo ci sono e hanno il tipo giusto;
- i campi con un `=` hanno un valore predefinito e sono facoltativi;
- gli errori dicono **quale campo** e **dove** (`corpo`, `query`, `indirizzo`): chi usa la tua API sa subito cosa correggere.

## Modelli dentro modelli

Un campo può essere a sua volta un modello, o una lista di modelli. Un `Modello` si usa anche da solo, per controllare dati che arrivano da altrove (un file, un database): se non vanno solleva `ErroreValidazione`.

```pit
importa server_web


classe Riga(server_web.Modello):
    articolo: tipo_testo
    quantita: tipo_intero = 1


classe Ordine(server_web.Modello):
    cliente: tipo_testo
    righe: list[Riga]


ordine = Ordine.da_dati({"cliente": "Ada", "righe": [{"articolo": "pane", "quantita": 2}, {"articolo": "latte"}]})
stampa(ordine.cliente, lunghezza_di(ordine.righe), ordine.righe[1].quantita)
prova:
    Ordine.da_dati({"cliente": "Ada", "righe": [{"quantita": 1}]})
eccetto server_web.ErroreValidazione come errore:
    stampa(errore.errori[0]["campo"])
```

```output
Ada 2 1
righe[0].articolo
```

## Gruppi di rotte e documentazione

Quando le rotte crescono si raggruppano con un prefisso. E dato che il server conosce già indirizzi, tipi e modelli, può **scrivere da solo la documentazione**: `app.documentazione()` crea la pagina `/docs` (da leggere) e `/openapi.json` (da dare a Swagger, Postman o a un generatore di client). La prima riga della docstring di una funzione diventa il suo titolo.

```pit
importa server_web

app = server_web.Applicazione(registro=Falso)
api = app.gruppo("/api/v1")


@api.ottieni("/ciao")
definisci ciao():
    """Saluta chi chiama."""
    ritorna {"ciao": "mondo"}


@api.ottieni("/prodotti/<codice>")
definisci prodotto(codice: tipo_intero):
    ritorna {"codice": codice}


app.documentazione("/docs", "Negozio", "1.0")
descrizione = app.openapi("Negozio", "1.0")
stampa(sorted(descrizione["paths"]))
stampa(descrizione["paths"]["/api/v1/ciao"]["get"]["summary"])
stampa(descrizione["paths"]["/api/v1/prodotti/{codice}"]["get"]["parameters"][0]["schema"])
```

```output
['/api/v1/ciao', '/api/v1/prodotti/{codice}']
Saluta chi chiama.
{'type': 'integer'}
```

Prova con un progetto **Sito web o API**: premi F5 e apri `/docs` dal link nella console.

## Esercizi

1. Una rotta `/area/<base>/<altezza>` con `base` e `altezza` decimali, che ritorna `{"area": ...}`. Controlla che `/area/3/4` dia 12.0 e che `/area/3/x` dia 422.
2. Un modello `Libro` con `titolo` (testo), `anno` (intero) e `letto` (vero/falso, predefinito falso), e una rotta `POST /libri` che ritorna il titolo con stato 201. Prova un libro valido e uno con l'anno scritto a lettere.
3. Raggruppa due rotte sotto `/negozio` e stampa gli indirizzi della documentazione, ordinati.

## Soluzioni

```pit
importa server_web

app = server_web.Applicazione(registro=Falso)


@app.rotta("/area/<base>/<altezza>")
definisci area(base: tipo_decimale, altezza: tipo_decimale):
    ritorna {"area": base * altezza}


stampa(app.simula("/area/3/4").dati)
stampa(app.simula("/area/3/x").stato)
```

```output
{'area': 12.0}
422
```

```pit
importa server_web

app = server_web.Applicazione(registro=Falso)


classe Libro(server_web.Modello):
    titolo: tipo_testo
    anno: tipo_intero
    letto: bool = Falso


@app.invia("/libri")
definisci nuovo_libro(libro: Libro):
    ritorna ({"titolo": libro.titolo}, 201)


stampa(app.simula("/libri", "POST", json={"titolo": "Il nome della rosa", "anno": 1980}).stato)
stampa(app.simula("/libri", "POST", json={"titolo": "Il nome della rosa", "anno": "millenovecentoottanta"}).stato)
```

```output
201
422
```

```pit
importa server_web

app = server_web.Applicazione(registro=Falso)
negozio = app.gruppo("/negozio")


@negozio.ottieni("/prodotti")
definisci prodotti():
    ritorna []


@negozio.ottieni("/ordini")
definisci ordini():
    ritorna []


stampa(sorted(app.openapi()["paths"]))
```

```output
['/negozio/ordini', '/negozio/prodotti']
```
