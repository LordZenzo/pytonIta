"""Server web per pytonIta: pagine, API in JSON e file statici con poche righe, senza installare niente.

    importa server_web

    app = server_web.Applicazione()

    @app.rotta("/")
    definisci home():
        ritorna "<h1>Ciao dal mio server!</h1>"

    @app.rotta("/saluta/<nome>")
    definisci saluta(nome):
        ritorna {"messaggio": "Ciao " + nome}            # un dizionario o una lista diventa JSON

    app.avvia(porta=8000)                                # http://127.0.0.1:8000/  (Ctrl+C o «Ferma» di PitStudio per spegnerlo)

Cosa ritorna una funzione di rotta:
  - un testo: pagina HTML;  un dizionario o una lista: JSON;  dei byte: dati grezzi;  Nessuno: risposta vuota (204);
  - una coppia (corpo, stato), per esempio ("Non trovato", 404);
  - un oggetto Risposta, per controllare tutto (tipo, intestazioni, cookie);  reindirizza("/altra") per cambiare pagina.
La funzione puo' chiedere `richiesta` (metodo, percorso, parametri, form, json, cookie...) e i pezzi variabili dell'indirizzo:
  "/utente/<nome>" (testo), "/articolo/<n:numero>" (intero), "/file/<percorso:resto>" (anche con le barre).
Le rotte rispondono a GET; per altri metodi: @app.rotta("/voci", metodi=["GET", "POST"]) oppure @app.invia("/voci").

Sicurezza: per default il server ascolta solo sul tuo computer (127.0.0.1). Con ascolta="0.0.0.0" lo vede tutta la rete:
fallo solo per provare, e mai con dati riservati. Non e' un server per Internet aperto al pubblico: per quello serve un
servizio di hosting con un server di produzione.
"""
import html as _html
import inspect as _ispeziona
import json as _json
import mimetypes as _mimetypes
import os as _os
import re as _re
import sys as _sistema
import threading as _thread
import time as _tempo
import urllib.parse as _url
import webbrowser as _browser
from http import HTTPStatus as _Stati
from http.cookies import SimpleCookie as _Cookie
from http.server import BaseHTTPRequestHandler as _Gestore, ThreadingHTTPServer as _Server

DIMENSIONE_MASSIMA = 10 * 1024 * 1024        # byte accettati nel corpo di una richiesta (10 MB)


class ErroreWeb(Exception):
    """Da sollevare in una rotta per rispondere con un errore: `solleva ErroreWeb(404, "Non c'e'")`."""

    def __init__(self, stato=500, messaggio=""):
        Exception.__init__(self, messaggio)
        self.stato = stato
        self.messaggio = messaggio or _frase(stato)


def _frase(stato):
    try:
        return _Stati(stato).phrase
    except ValueError:
        return "Errore"


class Richiesta:
    """Cio' che il browser ha chiesto. Si riceve nelle funzioni di rotta chiedendo un parametro `richiesta`."""

    def __init__(self, metodo, percorso, query, intestazioni, corpo, cliente):
        self.metodo = metodo
        self.percorso = percorso
        self.parametri = {k: v[0] for k, v in query.items()}          # ?a=1&b=2 -> {"a": "1", "b": "2"}
        self.parametri_multipli = query                                # ?a=1&a=2 -> {"a": ["1", "2"]}
        self.intestazioni = intestazioni
        self.corpo = corpo
        self.cliente = cliente
        tipo = (intestazioni.get("Content-Type") or "").split(";")[0].strip().lower()
        self.tipo = tipo
        self._json = None
        self._form = None
        cookie = _Cookie()
        try:
            cookie.load(intestazioni.get("Cookie") or "")
        except Exception:
            pass
        self.cookie = {k: m.value for k, m in cookie.items()}

    @property
    def testo(self):
        """Il corpo come testo (UTF-8)."""
        return self.corpo.decode("utf-8", "replace")

    @property
    def json(self):
        """Il corpo letto come JSON (dizionario, lista...); Nessuno se il corpo e' vuoto. Se non e' JSON valido risponde 400."""
        if self._json is None and self.corpo.strip():
            try:
                self._json = _json.loads(self.testo)
            except ValueError:
                raise ErroreWeb(400, "Il corpo della richiesta non e' un JSON valido")
        return self._json

    @property
    def form(self):
        """I campi di un modulo HTML inviato con POST (application/x-www-form-urlencoded): {"nome": "valore"}."""
        if self._form is None:
            if self.tipo == "application/x-www-form-urlencoded":
                self._form = {k: v[0] for k, v in _url.parse_qs(self.testo, keep_blank_values=True).items()}
            else:
                self._form = {}
        return self._form

    def valore(self, nome, predefinito=None):
        """Un valore dal form, dal JSON (se e' un dizionario) o dall'indirizzo, in questo ordine."""
        if nome in self.form:
            return self.form[nome]
        dati = self.json if self.tipo == "application/json" else None
        if isinstance(dati, dict) and nome in dati:
            return dati[nome]
        return self.parametri.get(nome, predefinito)


class Risposta:
    """Una risposta completa. Di solito basta ritornare un testo o un dizionario: serve per tipo, stato, intestazioni e cookie."""

    def __init__(self, corpo="", stato=200, tipo=None, intestazioni=None):
        self.stato = stato
        self.intestazioni = dict(intestazioni or {})
        self.cookie = []
        if isinstance(corpo, (dict, list)):
            corpo = _json.dumps(corpo, ensure_ascii=False)
            tipo = tipo or "application/json; charset=utf-8"
        if isinstance(corpo, str):
            self.corpo = corpo.encode("utf-8")
            tipo = tipo or "text/html; charset=utf-8"
        elif corpo is None:
            self.corpo = b""
        else:
            self.corpo = bytes(corpo)
            tipo = tipo or "application/octet-stream"
        self.tipo = tipo or "text/plain; charset=utf-8"

    @property
    def testo(self):
        """Il corpo della risposta come testo."""
        return self.corpo.decode("utf-8", "replace")

    @property
    def dati(self):
        """Il corpo della risposta letto come JSON (utile per provare le API)."""
        return _json.loads(self.testo)

    def imposta_cookie(self, nome, valore, durata=None, percorso="/", solo_http=True):
        """Chiede al browser di ricordare un cookie. durata: secondi (Nessuno = finche' il browser resta aperto)."""
        c = _Cookie()
        c[nome] = valore
        c[nome]["path"] = percorso
        if durata is not None:
            c[nome]["max-age"] = int(durata)
        if solo_http:
            c[nome]["httponly"] = True
        c[nome]["samesite"] = "Lax"
        self.cookie.append(c[nome].OutputString())
        return self

    def togli_cookie(self, nome, percorso="/"):
        return self.imposta_cookie(nome, "", durata=0, percorso=percorso)


def reindirizza(indirizzo, stato=302):
    """Manda il browser a un'altra pagina: `ritorna reindirizza("/grazie")`."""
    return Risposta("", stato, intestazioni={"Location": indirizzo})


def json_risposta(dati, stato=200):
    """Una risposta JSON con lo stato che scegli: `ritorna json_risposta({"errore": "manca il nome"}, 400)`."""
    return Risposta(dati, stato)


def pagina(modello, /, **valori):
    """Sostituisce {{ nome }} con i valori, senza rischi: i caratteri speciali (< > & ") vengono resi innocui.
    {{ nome|grezzo }} inserisce il valore cosi' com'e' (solo per HTML scritto da te). Un nome che manca resta vuoto."""
    def sostituisci(m):
        nome, _, filtro = m.group(1).strip().partition("|")
        valore = valori.get(nome.strip(), "")
        valore = "" if valore is None else str(valore)
        return valore if filtro.strip() == "grezzo" else _html.escape(valore)
    return _re.sub(r"\{\{\s*([^{}]+?)\s*\}\}", sostituisci, modello)


def carica_pagina(file, /, **valori):
    """Legge un file HTML (nella cartella del programma) e ci mette i valori, come pagina()."""
    with open(file, encoding="utf-8") as f:
        return pagina(f.read(), **valori)


_TIPI_PARAMETRO = ("testo", "str", "numero", "int", "resto", "path")


class _Rotta:
    def __init__(self, modello, metodi, funzione):
        self.modello = modello
        self.metodi = tuple(m.upper() for m in metodi)
        self.funzione = funzione
        self.tipi = {}
        pezzi = []
        for parte in _re.split(r"(<[^<>]+>)", modello):
            m = _re.fullmatch(r"<(\w+)(?::(\w+))?>", parte) if parte.startswith("<") else None
            if not m:
                pezzi.append(_re.escape(parte))
                continue
            nome, tipo = m.group(1), m.group(2) or "testo"
            if nome in _TIPI_PARAMETRO and tipo not in _TIPI_PARAMETRO:        # anche alla maniera di Flask: <int:n>
                nome, tipo = tipo, nome
            if tipo in ("numero", "int"):
                pezzi.append(f"(?P<{nome}>-?\\d+)")
                self.tipi[nome] = int
            elif tipo in ("resto", "path"):
                pezzi.append(f"(?P<{nome}>.+)")
            elif tipo in ("testo", "str"):
                pezzi.append(f"(?P<{nome}>[^/]+)")
            else:
                raise ValueError(f"tipo di parametro sconosciuto «{tipo}» in {modello!r} (usa testo, numero o resto)")
        self.regola = _re.compile("".join(pezzi) + "/?")
        firma = _ispeziona.signature(funzione)
        self.nomi = set(firma.parameters)
        self.accetta_tutto = any(p.kind is p.VAR_KEYWORD for p in firma.parameters.values())

    def corrisponde(self, percorso):
        m = self.regola.fullmatch(percorso)
        if not m:
            return None
        valori = {k: _url.unquote(v) for k, v in m.groupdict().items()}
        for nome, tipo in self.tipi.items():
            valori[nome] = tipo(valori[nome])
        return valori


def _tipo_file(percorso):
    tipo = _mimetypes.guess_type(percorso)[0] or "application/octet-stream"
    return tipo + ("; charset=utf-8" if tipo.startswith("text/") or tipo in ("application/javascript", "application/json") else "")


class Applicazione:
    """Il tuo sito: registra le rotte e poi `avvia()`.

    registro: Vero (predefinito) scrive una riga per ogni richiesta («GET /pagina 200»), cosi' la console di PitStudio la mostra."""

    def __init__(self, nome="app", registro=True):
        self.nome = nome
        self.registro = registro
        self._rotte = []
        self._statici = []
        self._gestori_errore = {}
        self._prima = []
        self.dati = {}                         # un posto dove tenere cio' che serve a piu' rotte (per esempio la connessione al database)

    # ---- registrazione
    def rotta(self, percorso, metodi=("GET",)):
        """Decoratore: collega un indirizzo a una funzione."""
        if not percorso.startswith("/"):
            raise ValueError(f"l'indirizzo deve cominciare con / (invece e' {percorso!r})")

        def registra(funzione):
            self._rotte.append(_Rotta(percorso, metodi, funzione))
            return funzione
        return registra

    def ottieni(self, percorso):
        return self.rotta(percorso, ("GET",))

    def invia(self, percorso):
        """Rotta che risponde a POST (l'invio di un modulo o di dati JSON)."""
        return self.rotta(percorso, ("POST",))

    def modifica(self, percorso):
        return self.rotta(percorso, ("PUT", "PATCH"))

    def elimina_rotta(self, percorso):
        return self.rotta(percorso, ("DELETE",))

    def statici(self, prefisso, cartella):
        """Serve i file di una cartella (css, immagini, script) sotto un indirizzo: statici("/statici", "cartella")."""
        self._statici.append((prefisso.rstrip("/") + "/", _os.path.abspath(cartella)))

    def errore(self, stato):
        """Decoratore: la tua pagina per un errore (per esempio 404): `@app.errore(404)`; la funzione riceve `richiesta` se la chiede."""
        def registra(funzione):
            self._gestori_errore[stato] = funzione
            return funzione
        return registra

    def prima_di_ogni_richiesta(self, funzione):
        """Decoratore: la funzione gira prima di ogni rotta (controlli, accessi); se ritorna qualcosa, quella e' la risposta."""
        self._prima.append(funzione)
        return funzione

    # ---- il lavoro vero
    def _chiama(self, funzione, richiesta, valori, nomi, accetta_tutto):
        argomenti = {k: v for k, v in valori.items() if accetta_tutto or k in nomi}
        if "richiesta" in nomi or accetta_tutto:
            argomenti["richiesta"] = richiesta
        return funzione(**argomenti)

    def _in_risposta(self, esito):
        if isinstance(esito, Risposta):
            return esito
        if isinstance(esito, tuple) and esito and len(esito) in (2, 3):
            risposta = Risposta(esito[0], esito[1])
            if len(esito) == 3:
                risposta.intestazioni.update(esito[2])
            return risposta
        if esito is None:
            return Risposta("", 204)
        return Risposta(esito)

    def _pagina_errore(self, richiesta, stato, messaggio=""):
        funzione = self._gestori_errore.get(stato)
        if funzione:
            try:
                risposta = self._in_risposta(self._chiama(funzione, richiesta, {}, set(_ispeziona.signature(funzione).parameters), False))
                risposta.stato = stato
                return risposta
            except Exception:
                pass
        if richiesta.percorso.startswith("/api") or "application/json" in (richiesta.intestazioni.get("Accept") or ""):
            return Risposta({"errore": messaggio or _frase(stato), "stato": stato}, stato)
        corpo = (f"<!doctype html><meta charset=utf-8><title>{stato}</title><body style='font-family:sans-serif;margin:3em'>"
                 f"<h1>{stato} &middot; {_html.escape(_frase(stato))}</h1><p>{_html.escape(messaggio)}</p></body>")
        return Risposta(corpo, stato)

    def _file_statico(self, richiesta):
        for prefisso, cartella in self._statici:
            if richiesta.percorso.startswith(prefisso):
                relativo = _url.unquote(richiesta.percorso[len(prefisso):])
                percorso = _os.path.abspath(_os.path.join(cartella, relativo))
                if percorso != cartella and not percorso.startswith(cartella + _os.sep):
                    raise ErroreWeb(403, "Percorso non permesso")
                if _os.path.isfile(percorso):
                    with open(percorso, "rb") as f:
                        return Risposta(f.read(), 200, _tipo_file(percorso))
                raise ErroreWeb(404, "File non trovato")
        return None

    def risposta_a(self, richiesta):
        """Trova la rotta giusta per una richiesta e ne ricava la risposta (non scrive nulla sulla rete: si puo' provare anche da soli)."""
        try:
            for prima in self._prima:
                esito = self._chiama(prima, richiesta, {}, set(_ispeziona.signature(prima).parameters), False)
                if esito is not None:
                    return self._in_risposta(esito)
            metodi_permessi = set()
            for rotta in self._rotte:
                valori = rotta.corrisponde(richiesta.percorso)
                if valori is None:
                    continue
                metodo = "GET" if richiesta.metodo == "HEAD" else richiesta.metodo
                if metodo in rotta.metodi:
                    return self._in_risposta(self._chiama(rotta.funzione, richiesta, valori, rotta.nomi, rotta.accetta_tutto))
                metodi_permessi.update(rotta.metodi)
            if richiesta.metodo in ("GET", "HEAD"):
                statico = self._file_statico(richiesta)
                if statico:
                    return statico
            if richiesta.metodo == "OPTIONS" and metodi_permessi:
                return Risposta("", 204, intestazioni={"Allow": ", ".join(sorted(metodi_permessi | {"OPTIONS"}))})
            if metodi_permessi:
                risposta = self._pagina_errore(richiesta, 405, "Questo indirizzo non accetta " + richiesta.metodo)
                risposta.intestazioni["Allow"] = ", ".join(sorted(metodi_permessi))
                return risposta
            return self._pagina_errore(richiesta, 404, "Pagina non trovata: " + richiesta.percorso)
        except ErroreWeb as errore:
            return self._pagina_errore(richiesta, errore.stato, errore.messaggio)
        except Exception as errore:
            import traceback
            traceback.print_exc()
            return self._pagina_errore(richiesta, 500, "Errore nel programma: " + type(errore).__name__ + ": " + str(errore))

    def simula(self, percorso, metodo="GET", json=None, form=None, intestazioni=None, cookie=None):
        """Prova una rotta senza accendere il server e senza rete: ritorna la Risposta (stato, testo, dati, intestazioni).

            r = app.simula("/saluta/Ada")           r.stato -> 200,  r.dati -> {"messaggio": "Ciao Ada"}
            r = app.simula("/voci", "POST", json={"titolo": "pane"})
            r = app.simula("/modulo", "POST", form={"nome": "Ada"})
        Serve per imparare e per i test automatici del tuo sito."""
        parti = _url.urlsplit(percorso)
        intestazioni = dict(intestazioni or {})
        corpo = b""
        if json is not None:
            corpo = _json.dumps(json).encode("utf-8")
            intestazioni["Content-Type"] = "application/json"
        elif form is not None:
            corpo = _url.urlencode(form).encode("utf-8")
            intestazioni["Content-Type"] = "application/x-www-form-urlencoded"
        if cookie:
            intestazioni["Cookie"] = "; ".join(f"{k}={v}" for k, v in cookie.items())
        richiesta = Richiesta(metodo.upper(), _url.unquote(parti.path), _url.parse_qs(parti.query, keep_blank_values=True), intestazioni, corpo, "simulato")
        return self.risposta_a(richiesta)

    def _crea_server(self, porta, ascolta):
        app = self

        class Gestore(_Gestore):
            protocol_version = "HTTP/1.1"

            def _servi(self):
                inizio = _tempo.time()
                url = _url.urlsplit(self.path)
                try:
                    lunghezza = int(self.headers.get("Content-Length") or 0)
                except ValueError:
                    lunghezza = 0
                if lunghezza > DIMENSIONE_MASSIMA:
                    corpo = b""
                    richiesta = Richiesta(self.command, _url.unquote(url.path), {}, self.headers, corpo, self.client_address[0])
                    risposta = app._pagina_errore(richiesta, 413, "Richiesta troppo grande")
                    self.close_connection = True
                else:
                    corpo = self.rfile.read(lunghezza) if lunghezza > 0 else b""
                    richiesta = Richiesta(self.command, _url.unquote(url.path), _url.parse_qs(url.query, keep_blank_values=True), self.headers, corpo,
                                          self.client_address[0])
                    risposta = app.risposta_a(richiesta)
                self.send_response(risposta.stato)
                self.send_header("Content-Type", risposta.tipo)
                self.send_header("Content-Length", str(len(risposta.corpo)))
                self.send_header("Cache-Control", "no-store")
                for k, v in risposta.intestazioni.items():
                    self.send_header(k, v)
                for c in risposta.cookie:
                    self.send_header("Set-Cookie", c)
                self.end_headers()
                if self.command != "HEAD" and risposta.stato not in (204, 304):
                    self.wfile.write(risposta.corpo)
                if app.registro:
                    print(f"{self.command} {self.path} {risposta.stato} ({int((_tempo.time() - inizio) * 1000)} ms)", flush=True)

            do_GET = do_POST = do_PUT = do_PATCH = do_DELETE = do_HEAD = do_OPTIONS = _servi

            def log_message(self, formato, *argomenti):        # il registro lo scriviamo noi, in italiano
                pass

        _Server.allow_reuse_address = True
        server = _Server((ascolta, porta), Gestore)
        server.daemon_threads = True
        return server

    def avvia(self, porta=8000, ascolta="127.0.0.1", apri_browser=False):
        """Accende il server e resta qui finche' non lo spegni (Ctrl+C, oppure «Ferma» in PitStudio). Scrive l'indirizzo, cosi' si puo' cliccare."""
        server = self._crea_server(porta, ascolta)
        indirizzo = f"http://{'127.0.0.1' if ascolta in ('0.0.0.0', '') else ascolta}:{server.server_address[1]}/"
        print(f"Server in ascolto su {indirizzo}  (per spegnerlo: Ctrl+C o Ferma)", flush=True)
        if ascolta in ("0.0.0.0", ""):
            print("Attenzione: lo vedono tutti i computer della rete.", flush=True)
        if apri_browser:
            _thread.Timer(0.4, lambda: _browser.open(indirizzo)).start()
        try:
            server.serve_forever(poll_interval=0.2)
        except KeyboardInterrupt:
            print("Server spento.", flush=True)
        finally:
            server.server_close()

    def avvia_in_sottofondo(self, porta=0, ascolta="127.0.0.1"):
        """Accende il server senza bloccare il programma (utile con una finestra tkinter, o per le prove). porta=0 sceglie una porta libera.
        Ritorna un oggetto con .indirizzo, .porta e .ferma()."""
        server = self._crea_server(porta, ascolta)
        filo = _thread.Thread(target=lambda: server.serve_forever(poll_interval=0.1), daemon=True)
        filo.start()
        return ServerAvviato(server, filo)


class ServerAvviato:
    """Un server acceso in sottofondo da Applicazione.avvia_in_sottofondo."""

    def __init__(self, server, filo):
        self._server = server
        self._filo = filo
        self.porta = server.server_address[1]
        self.indirizzo = f"http://127.0.0.1:{self.porta}"

    def ferma(self):
        self._server.shutdown()
        self._server.server_close()
        self._filo.join(3)

    def __enter__(self):
        return self

    def __exit__(self, *errori):
        self.ferma()
