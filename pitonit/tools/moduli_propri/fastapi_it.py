"""FastAPI con i nomi italiani: la strada per le applicazioni web piu' grandi (richiede `fastapi` e `uvicorn`).

    importa fastapi_it

    app = fastapi_it.Applicazione("Le mie voci")

    classe Voce(fastapi_it.Modello):
        titolo: tipo_testo
        quantita: tipo_intero = 1

    @app.ottieni("/voci/{numero}")
    definisci leggi_voce(numero: tipo_intero, dettagli: bool = Falso):      # ?dettagli=true dall'indirizzo
        ritorna {"numero": numero, "dettagli": dettagli}

    @app.invia("/voci", stato=201)
    definisci crea_voce(voce: Voce):                                       # il JSON e' controllato da pydantic (422 se sbagliato)
        ritorna voce.a_dizionario()

    app.avvia(porta=8000)          # documentazione automatica: http://127.0.0.1:8000/docs

E' lo stesso FastAPI di tutti (`app.app` e' l'oggetto FastAPI vero: middleware, dipendenze, WebSocket... funzionano come nella sua
documentazione): qui ci sono solo i nomi in italiano e l'avvio con uvicorn che scrive l'indirizzo cliccabile nella console di PitStudio.

Per installare i due pacchetti: in PitStudio, pannello «Pacchetti» -> cerca `fastapi` e `uvicorn` -> Installa (oppure `pip install fastapi uvicorn`).
Il modulo `server_web` (senza pacchetti da installare) e' piu' semplice e basta per molti progetti: si puo' anche usare insieme a questo con
`app.monta("/vecchio", altra_app)`, e un'applicazione server_web si puo' dare a uvicorn con `uvicorn.run(app.asgi)`.
"""
import re as _re
import threading as _thread
import time as _tempo

try:
    import fastapi as _fastapi
    import pydantic as _pydantic
    import uvicorn as _uvicorn
    from fastapi.responses import HTMLResponse as _Html, JSONResponse as _Json, RedirectResponse as _Reindirizza
    from fastapi.staticfiles import StaticFiles as _StaticFiles
    MANCA = None
except ImportError as _errore:
    _fastapi = _pydantic = _uvicorn = None
    MANCA = str(_errore)


class MancaFastAPI(ImportError):
    """FastAPI (o uvicorn) non e' installato."""


def _controlla():
    if MANCA is not None:
        raise MancaFastAPI("Serve FastAPI: installa i pacchetti «fastapi» e «uvicorn» (in PitStudio: pannello Pacchetti, oppure `pip install fastapi uvicorn`). "
                           f"Dettaglio: {MANCA}")


if _pydantic is not None:
    class Modello(_pydantic.BaseModel):
        """La forma dei dati ricevuti o restituiti (pydantic): campi con tipo e valore predefinito. Ha anche a_dizionario() e da_dati()."""

        def a_dizionario(self):
            return self.model_dump()

        @classmethod
        def da_dati(cls, dati):
            return cls.model_validate(dati)
else:
    class Modello:
        def __init_subclass__(cls, **k):
            _controlla()

        def __init__(self, *a, **k):
            _controlla()

if _fastapi is not None:
    class ErroreWeb(_fastapi.HTTPException):
        """Da sollevare in una rotta per rispondere con un errore: `solleva ErroreWeb(404, "Non c'e'")`."""

        def __init__(self, stato=500, messaggio="", intestazioni=None):
            from http import HTTPStatus
            try:
                frase = HTTPStatus(stato).phrase
            except ValueError:
                frase = "Errore"
            _fastapi.HTTPException.__init__(self, status_code=stato, detail=messaggio or frase, headers=intestazioni)

    Richiesta = _fastapi.Request
    Dipende = _fastapi.Depends
    Query = _fastapi.Query
    Corpo = _fastapi.Body
    Intestazione = _fastapi.Header
    Cookie = _fastapi.Cookie
    Percorso = _fastapi.Path
    File = _fastapi.File
    FileCaricato = _fastapi.UploadFile
    Modulo = _fastapi.Form
    TaskInSottofondo = _fastapi.BackgroundTasks

    def reindirizza(indirizzo, stato=302):
        """Manda il browser a un'altra pagina: `ritorna reindirizza("/grazie")`."""
        return _Reindirizza(indirizzo, status_code=stato)

    def json_risposta(dati, stato=200):
        return _Json(dati, status_code=stato)

    def pagina_html(testo, stato=200):
        return _Html(testo, status_code=stato)
else:
    ErroreWeb = Richiesta = Dipende = Query = Corpo = Intestazione = Cookie = Percorso = File = FileCaricato = Modulo = TaskInSottofondo = None

    def reindirizza(*a, **k):
        _controlla()

    json_risposta = pagina_html = reindirizza

_OPZIONI = {"stato": "status_code", "riassunto": "summary", "etichette": "tags", "descrizione": "description", "modello_risposta": "response_model",
            "nome": "name", "deprecata": "deprecated", "dipendenze": "dependencies"}


def _opzioni(opzioni):
    return {_OPZIONI.get(k, k): v for k, v in opzioni.items()}


def _percorso(percorso):
    """/utente/<nome>, /articolo/<n:numero> e /file/<p:resto> (alla maniera di server_web) diventano /utente/{nome}, /articolo/{n}, /file/{p:path}."""
    def cambia(m):
        nome, tipo = m.group(1), m.group(2)
        return "{" + nome + (":path" if tipo in ("resto", "path") else "") + "}"
    return _re.sub(r"<(\w+)(?::(\w+))?>", cambia, percorso)


class Applicazione:
    """Un'applicazione FastAPI con i nomi italiani. `app.app` e' l'oggetto FastAPI vero."""

    def __init__(self, titolo="API", versione="1.0", descrizione="", registro=True):
        _controlla()
        self.app = _fastapi.FastAPI(title=titolo, version=versione, description=descrizione)
        self.titolo = titolo
        self.registro = registro
        if registro:
            @self.app.middleware("http")
            async def scrivi_registro(richiesta, prossimo):
                inizio = _tempo.time()
                risposta = await prossimo(richiesta)
                print(f"{richiesta.method} {richiesta.url.path} {risposta.status_code} ({int((_tempo.time() - inizio) * 1000)} ms)", flush=True)
                return risposta

    # ---- rotte
    def rotta(self, percorso, metodi=("GET",), **opzioni):
        """Decoratore: collega un indirizzo a una funzione. Opzioni (anche in italiano): stato, riassunto, etichette, descrizione, modello_risposta."""
        return self.app.api_route(_percorso(percorso), methods=[m.upper() for m in metodi], **_opzioni(opzioni))

    def ottieni(self, percorso, **opzioni):
        return self.rotta(percorso, ("GET",), **opzioni)

    def invia(self, percorso, **opzioni):
        return self.rotta(percorso, ("POST",), **opzioni)

    def modifica(self, percorso, **opzioni):
        return self.rotta(percorso, ("PUT", "PATCH"), **opzioni)

    def elimina_rotta(self, percorso, **opzioni):
        return self.rotta(percorso, ("DELETE",), **opzioni)

    def gruppo(self, prefisso, **opzioni):
        """Un gruppo di rotte con un prefisso comune: `api = app.gruppo("/api")` e poi `@api.ottieni("/voci")` risponde a /api/voci."""
        return _GruppoFastAPI(self, prefisso.rstrip("/"), _opzioni(opzioni))

    def statici(self, prefisso, cartella):
        """Serve i file di una cartella sotto un indirizzo."""
        self.app.mount(prefisso.rstrip("/"), _StaticFiles(directory=cartella), name="statici" + prefisso.replace("/", "_"))

    def monta(self, prefisso, applicazione):
        """Monta un'altra applicazione sotto un prefisso: una server_web.Applicazione (o qualsiasi applicazione ASGI)."""
        asgi = getattr(applicazione, "asgi", applicazione)
        self.app.mount(prefisso.rstrip("/") or "/", asgi)

    def errore(self, stato):
        """Decoratore: la tua risposta per un errore (per esempio 404)."""
        return self.app.exception_handler(stato)

    def all_avvio(self, funzione):
        self.app.add_event_handler("startup", funzione)
        return funzione

    def alla_chiusura(self, funzione):
        self.app.add_event_handler("shutdown", funzione)
        return funzione

    # ---- avvio
    def avvia(self, porta=8000, ascolta="127.0.0.1", ricarica=False, apri_browser=False):
        """Accende il server (uvicorn) e resta qui finche' non lo spegni (Ctrl+C, oppure «Ferma» in PitStudio)."""
        host = "127.0.0.1" if ascolta in ("0.0.0.0", "") else ascolta
        indirizzo = f"http://{host}:{porta}/"
        print(f"Server in ascolto su {indirizzo}  (per spegnerlo: Ctrl+C o Ferma)", flush=True)
        print(f"Documentazione: {indirizzo}docs", flush=True)
        if ascolta in ("0.0.0.0", ""):
            print("Attenzione: lo vedono tutti i computer della rete.", flush=True)
        if apri_browser:
            import webbrowser
            _thread.Timer(0.8, lambda: webbrowser.open(indirizzo)).start()
        _uvicorn.run(self.app, host=ascolta, port=porta, log_level="warning", reload=False)

    def avvia_in_sottofondo(self, porta=0, ascolta="127.0.0.1"):
        """Accende il server senza bloccare il programma (per le prove o per le finestre). porta=0 sceglie una porta libera. Ritorna un oggetto con .porta, .indirizzo e .ferma()."""
        configurazione = _uvicorn.Config(self.app, host=ascolta, port=porta, log_level="warning")
        server = _uvicorn.Server(configurazione)
        filo = _thread.Thread(target=server.run, daemon=True)
        filo.start()
        scadenza = _tempo.time() + 15
        while not server.started and _tempo.time() < scadenza:
            _tempo.sleep(0.02)
        if not server.started:
            raise RuntimeError("il server non e' partito")
        porta_vera = server.servers[0].sockets[0].getsockname()[1]
        return _ServerAvviato(server, filo, porta_vera)


class _GruppoFastAPI:
    def __init__(self, applicazione, prefisso, opzioni):
        self._app = applicazione
        self.prefisso = prefisso
        self._opzioni = opzioni

    def rotta(self, percorso, metodi=("GET",), **opzioni):
        def registra(funzione):
            self._app.app.add_api_route(self.prefisso + _percorso(percorso), funzione, methods=[m.upper() for m in metodi], **{**self._opzioni, **_opzioni(opzioni)})
            return funzione
        return registra

    def ottieni(self, percorso, **opzioni):
        return self.rotta(percorso, ("GET",), **opzioni)

    def invia(self, percorso, **opzioni):
        return self.rotta(percorso, ("POST",), **opzioni)

    def modifica(self, percorso, **opzioni):
        return self.rotta(percorso, ("PUT", "PATCH"), **opzioni)

    def elimina_rotta(self, percorso, **opzioni):
        return self.rotta(percorso, ("DELETE",), **opzioni)


class _ServerAvviato:
    def __init__(self, server, filo, porta):
        self._server = server
        self._filo = filo
        self.porta = porta
        self.indirizzo = f"http://127.0.0.1:{porta}"

    def ferma(self):
        self._server.should_exit = True
        self._filo.join(10)

    def __enter__(self):
        return self

    def __exit__(self, *errori):
        self.ferma()
