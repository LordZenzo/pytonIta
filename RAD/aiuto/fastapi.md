# FastAPI in italiano

**FastAPI** è il framework più usato per costruire API in Python: tipi controllati da `pydantic`, documentazione automatica (Swagger), funzioni asincrone, WebSocket, dipendenze. Il modulo **`fastapi_it`** lo usa con i **nomi in italiano** e avvia il server come gli altri programmi di PitStudio (l'indirizzo compare nella console ed è cliccabile).

Non è incluso in PitStudio: prima servono due pacchetti.

## Installare i pacchetti

In PitStudio: pannello **Pacchetti** → cerca `fastapi` e `uvicorn` → *Installa* (finiscono nella cartella dei pacchetti del progetto). Oppure da un terminale: `pip install fastapi uvicorn`. Senza i pacchetti `import fastapi_it` funziona, ma `fastapi_it.Applicazione()` dice cosa manca.

## Un esempio

```pit sintassi
importa fastapi_it

app = fastapi_it.Applicazione("Le mie voci", "1.0")


classe Voce(fastapi_it.Modello):
    titolo: tipo_testo
    quantita: tipo_intero = 1


@app.ottieni("/voci/{numero}")
definisci leggi_voce(numero: tipo_intero, dettagli: bool = Falso):
    ritorna {"numero": numero, "dettagli": dettagli}


@app.invia("/voci", stato=201, riassunto="Crea una voce")
definisci crea_voce(voce: Voce):
    ritorna voce.a_dizionario()


app.avvia(porta=8000)
```

**F5**, clic sull'indirizzo nella console, e vai su **`/docs`**: FastAPI ha già scritto la documentazione, con i pulsanti per provare ogni indirizzo. (La pagina `/docs` carica il suo aspetto da Internet: offline si vede come testo semplice; `/openapi.json` funziona sempre.)

## I nomi italiani

| fastapi_it | In FastAPI |
|---|---|
| `Applicazione(titolo, versione, descrizione)` | `FastAPI(title=…, version=…)` (l'oggetto vero è `app.app`) |
| `@app.rotta`, `@app.ottieni`, `@app.invia`, `@app.modifica`, `@app.elimina_rotta` | `api_route`, `get`, `post`, `put/patch`, `delete` |
| opzioni `stato`, `riassunto`, `etichette`, `descrizione`, `modello_risposta` | `status_code`, `summary`, `tags`, `description`, `response_model` |
| `app.gruppo("/api")` | un gruppo con prefisso (come un `APIRouter`) |
| `Modello` | `pydantic.BaseModel` (più `a_dizionario()` e `da_dati()`) |
| `ErroreWeb(stato, messaggio)` | `HTTPException` |
| `reindirizza`, `json_risposta`, `pagina_html` | `RedirectResponse`, `JSONResponse`, `HTMLResponse` |
| `Query`, `Corpo`, `Intestazione`, `Cookie`, `Percorso`, `Dipende`, `File`, `Modulo`, `FileCaricato`, `TaskInSottofondo` | `Query`, `Body`, `Header`, `Cookie`, `Path`, `Depends`, `File`, `Form`, `UploadFile`, `BackgroundTasks` |
| `app.statici(prefisso, cartella)` | `mount(…, StaticFiles(…))` |
| `app.all_avvio`, `app.alla_chiusura` | eventi `startup` e `shutdown` |
| `app.avvia(porta, ascolta)`, `app.avvia_in_sottofondo()` | `uvicorn.run(…)` |

Gli indirizzi si possono scrivere alla maniera di FastAPI (`/voci/{numero}`) o di `server_web` (`/voci/<numero>`, `/articolo/<n:numero>`, `/file/<p:resto>`).

## Quale scegliere?

| | `server_web` | `fastapi_it` |
|---|---|---|
| installazione | niente | `fastapi` e `uvicorn` |
| tipi, modelli e 422 | sì | sì (pydantic: più completo) |
| documentazione `/docs` | sì (semplice, offline) | sì (Swagger) |
| pagine HTML con modelli | sì (con cicli e sessioni) | no (si usa Jinja2 a parte) |
| sessioni, accesso, CSRF | integrati | da aggiungere (o con librerie) |
| WebSocket, dipendenze, background | no | sì |
| per cominciare | **sì** | quando serve un'API grande o l'ecosistema di FastAPI |

## Insieme

- Una applicazione `server_web` si può **montare dentro** FastAPI: `app.monta("/vecchio", altra_app)`.
- Una applicazione `server_web` si può dare a **uvicorn** senza FastAPI: `uvicorn.run(altra_app.asgi)`.
- Per la produzione: `uvicorn` dietro un proxy con HTTPS, come per qualsiasi applicazione FastAPI.

## Esportare e creare l'eseguibile

I progetti con `fastapi_it` si esportano come Python: `requirements.txt` elenca `fastapi`, `uvicorn` e `pydantic`, e *Crea l'eseguibile* li include nel programma.
