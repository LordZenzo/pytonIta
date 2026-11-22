# Lezione 28 · Accessi e sicurezza

**Obiettivo:** far ricordare al sito chi sei (sessioni), proteggere le pagine con una password, difendersi dai moduli falsi (CSRF) e scrivere pagine con cicli e condizioni.

## Sessioni

Il web **non ricorda niente**: ogni richiesta è nuova. Per far ricordare qualcosa al sito (chi ha fatto l'accesso, il carrello…) si usa la **sessione**: un dizionario, `richiesta.sessione`, che il browser si porta dietro in un **cookie firmato**. Il visitatore può leggerlo ma, non avendo la **chiave segreta** del server, non può modificarlo: se ci prova, il cookie viene ignorato.

```pit
importa server_web

app = server_web.Applicazione(registro=Falso)
app.configura(chiave_segreta="una chiave lunga e riservata per imparare")


@app.rotta("/visite")
definisci visite(richiesta):
    richiesta.sessione["numero"] = richiesta.sessione.get("numero", 0) + 1
    ritorna {"visite": richiesta.sessione["numero"]}


cliente = app.cliente()
stampa(cliente.ottieni("/visite").dati)
stampa(cliente.ottieni("/visite").dati)
altro = app.cliente()
stampa(altro.ottieni("/visite").dati)
```

```output
{'visite': 1}
{'visite': 2}
{'visite': 1}
```

`app.cliente()` è un **browser finto** per le prove: ricorda i cookie come un browser vero, e così si prova un percorso intero senza aprire niente. Due clienti hanno due sessioni diverse.

Regole per la sessione: la chiave segreta va scelta lunga (almeno 16 caratteri), tenuta **riservata** e **non scritta nei file che pubblichi**; nella sessione si tengono poche cose (l'identificativo dell'utente, non un intero profilo: il cookie arriva a circa 4 KB).

## Password e accesso

Le password **non si salvano mai in chiaro**: si salva una **cifratura** che non si può invertire, e al momento dell'accesso si cifra quella scritta e si confronta. `cifra_password` e `verifica_password` lo fanno con un metodo robusto (scrypt, con un sale diverso per ogni password).

```pit
importa server_web

cifrata = server_web.cifra_password("segreta123")
stampa(cifrata != "segreta123")
stampa(server_web.verifica_password("segreta123", cifrata), server_web.verifica_password("altra", cifrata))
stampa(server_web.cifra_password("segreta123") != cifrata)
```

```output
Vero
Vero Falso
Vero
```

L'ultima riga mostra il **sale**: la stessa password, cifrata due volte, dà due testi diversi, quindi un ladro di database non può riconoscere chi ha la stessa password.

Ecco un accesso completo: `app.accedi` segna chi sei in sessione e `@app.richiede_accesso` protegge una pagina.

```pit
importa server_web

app = server_web.Applicazione(registro=Falso)
app.configura(chiave_segreta="una chiave lunga e riservata per imparare")
UTENTI = {"ada": server_web.cifra_password("segreta123")}


@app.invia("/accedi")
definisci accedi(richiesta):
    nome = richiesta.form.get("nome", "")
    se nome in UTENTI e server_web.verifica_password(richiesta.form.get("password", ""), UTENTI[nome]):
        app.accedi(richiesta, nome)
        ritorna server_web.reindirizza("/profilo")
    ritorna ("Credenziali sbagliate", 401)


@app.rotta("/profilo")
@app.richiede_accesso
definisci profilo(richiesta):
    ritorna {"utente": richiesta.utente}


cliente = app.cliente()
stampa(cliente.ottieni("/profilo").stato)
stampa(cliente.invia("/accedi", form={"nome": "ada", "password": "sbagliata"}).stato)
stampa(cliente.invia("/accedi", form={"nome": "ada", "password": "segreta123"}).stato)
stampa(cliente.ottieni("/profilo").dati)
```

```output
302
401
302
{'utente': 'ada'}
```

Chi non ha fatto l'accesso viene mandato alla pagina `/accedi` (302); per le API, se l'indirizzo comincia con `/api`, riceve 401. Per i **ruoli**: `@app.richiede_accesso(ruolo="admin")` e `app.accedi(richiesta, nome, ruoli=["admin"])`. Una password sbagliata dà sempre lo stesso messaggio, senza dire se è sbagliato il nome o la password.

## Il codice CSRF

Un sito malvagio potrebbe far inviare al **tuo** browser un modulo verso il **tuo** sito (dove sei già entrato) e fargli fare cose a tua insaputa: si chiama **CSRF**. La difesa: ogni modulo contiene un **codice segreto** che solo le tue pagine conoscono; il server rifiuta i POST senza il codice giusto. Si accende con `csrf=Vero` e si mette `{{ campo_csrf }}` in ogni modulo (per le API: l'intestazione `X-CSRF-Token`).

```pit
importa server_web

app = server_web.Applicazione(registro=Falso)
app.configura(chiave_segreta="una chiave lunga e riservata per imparare", csrf=Vero)


@app.rotta("/modulo")
definisci modulo(richiesta):
    ritorna "<form method=post>" + richiesta.campo_csrf + "</form>"


@app.invia("/salva")
definisci salva():
    ritorna "salvato"


cliente = app.cliente()
stampa(cliente.invia("/salva").stato)
cliente.ottieni("/modulo")
stampa(cliente.invia("/salva", form={"csrf": cliente.token_csrf}).stato)
```

```output
403
200
```

## Modelli di pagina

Finora le pagine erano testi. Per pagine vere servono **cicli e condizioni** dentro l'HTML: `app.mostra("pagina.html", richiesta, nome=valore)` legge un file dalla cartella delle pagine (`app.configura(cartella_pagine="pagine")`); `server_web.pagina(testo, nome=valore)` fa lo stesso su un testo.

```pit
importa server_web

modello = """<ul>
{% per voce in voci %}<li>{{ ciclo.indice }}. {{ voce.nome|maiuscolo }}{% se voce.prezzo > 1 %} (caro){% fine %}</li>
{% altrimenti %}<li>nessuna voce</li>
{% fine %}</ul>"""
stampa(server_web.pagina(modello, voci=[{"nome": "pane", "prezzo": 1}, {"nome": "caffè", "prezzo": 2.5}]))
stampa(server_web.pagina(modello, voci=[]))
```

```output
<ul>
<li>1. PANE</li>
<li>2. CAFFÈ (caro)</li>
</ul>
<ul>
<li>nessuna voce</li>
</ul>
```

- `{{ valore }}` stampa un valore, **reso innocuo**; i **filtri** (`|maiuscolo`, `|tronca(20)`, `|predefinito("n/d")`…) lo trasformano;
- `{% se … %}` / `{% altrimenti_se … %}` / `{% altrimenti %}` / `{% fine %}`: condizioni, con `e`, `o`, `non`;
- `{% per x in elenco %}` … `{% altrimenti %}` (se l'elenco è vuoto) … `{% fine %}`: cicli, con `ciclo.indice`, `ciclo.primo`, `ciclo.ultimo`;
- `{% estende "base.html" %}` e `{% blocco corpo %}…{% fine %}`: una **pagina base** con il menu e l'aspetto, e le altre pagine che ne riempiono i blocchi; `{% includi "menu.html" %}` inserisce un pezzo.

Dentro un modello non si può far eseguire codice a piacere: le espressioni sono controllate, ed è una difesa in più.

## Mettere il sito in produzione

`app.avvia()` va benissimo per imparare e per strumenti locali, ma **un sito aperto a tutti su Internet** ha bisogno di più:

1. un **server di produzione** al posto di `avvia()`: l'applicazione stessa è un'app WSGI (`waitress.serve(app, port=8000)`, `gunicorn`) e ha un'interfaccia ASGI (`uvicorn.run(app.asgi)`);
2. **HTTPS** (di solito con un proxy come Caddy o nginx davanti, che gestisce il certificato) e `configura(cookie_sicuro=Vero)`;
3. una **chiave segreta vera**, letta da una variabile d'ambiente o da un file fuori dal progetto;
4. `csrf=Vero`, password cifrate e **limiti di tentativi** sull'accesso (`server_web` non li fa da solo);
5. aggiornamenti, copie di sicurezza del database e un controllo di ciò che finisce nei registri.

Per progetti grandi, con tanti utenti e tante regole, può valere la pena passare a un framework più completo: vedi [FastAPI in italiano](#fastapi).

## Esercizi

1. Una rotta `POST /nome` che ricorda in sessione il nome inviato in un modulo, e una `GET /saluto` che risponde `Ciao NOME` (o `Ciao ospite` se non c'è). Provale con un cliente.
2. Con `server_web.pagina`, stampa un elenco numerato `1-a, 2-b, 3-c` dalla lista `["a", "b", "c"]` (senza la virgola dopo l'ultimo).
3. Una pagina `/riservata` solo per il ruolo `admin`: un cliente senza accesso va alla pagina di accesso (302), uno con il ruolo sbagliato riceve 403, uno con il ruolo giusto vede la pagina.

## Soluzioni

```pit
importa server_web

app = server_web.Applicazione(registro=Falso)
app.configura(chiave_segreta="una chiave lunga e riservata per imparare")


@app.invia("/nome")
definisci imposta_nome(richiesta):
    richiesta.sessione["nome"] = richiesta.form.get("nome", "sconosciuto")
    ritorna "ok"


@app.rotta("/saluto")
definisci saluto(richiesta):
    ritorna "Ciao " + richiesta.sessione.get("nome", "ospite")


cliente = app.cliente()
stampa(cliente.ottieni("/saluto").testo)
cliente.invia("/nome", form={"nome": "Ada"})
stampa(cliente.ottieni("/saluto").testo)
```

```output
Ciao ospite
Ciao Ada
```

```pit
importa server_web

modello = "{% per voce in cose %}{{ ciclo.indice }}-{{ voce }}{% se non ciclo.ultimo %}, {% fine %}{% fine %}"
stampa(server_web.pagina(modello, cose=["a", "b", "c"]))
```

```output
1-a, 2-b, 3-c
```

```pit
importa server_web

app = server_web.Applicazione(registro=Falso)
app.configura(chiave_segreta="una chiave lunga e riservata per imparare")


@app.rotta("/riservata")
@app.richiede_accesso(ruolo="admin")
definisci riservata():
    ritorna "segreto"


cliente = app.cliente()
stampa(cliente.ottieni("/riservata").stato)
cliente.imposta_sessione(utente="ada", ruoli=["lettore"])
stampa(cliente.ottieni("/riservata").stato)
cliente.imposta_sessione(ruoli=["admin"])
stampa(cliente.ottieni("/riservata").testo)
```

```output
302
403
segreto
```
