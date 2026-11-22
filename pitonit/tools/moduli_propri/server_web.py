"""Server web per pytonIta: pagine, API in JSON, sessioni e accessi, modelli di pagina e documentazione automatica, senza installare niente.

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

Come un framework (stile FastAPI/Flask):
  - parametri con tipo: `definisci voce(id: tipo_intero, q: tipo_testo = "")` legge `id` dall'indirizzo e `?q=` dalla richiesta, li converte
    e risponde 422 con la spiegazione se non vanno bene;
  - modelli di dati: `classe Voce(server_web.Modello): titolo: tipo_testo; fatto: bool = Falso` e `definisci nuova(voce: Voce)` riceve il JSON gia' validato;
  - gruppi di rotte: `api = app.gruppo("/api")`; sessioni firmate, protezione CSRF, accesso con password cifrate;
  - modelli di pagina con cicli, condizioni, ereditarieta' (`app.mostra("pagina.html", ...)`) e file inviati con i moduli;
  - documentazione automatica in /docs e /openapi.json (`app.documentazione()`);
  - WSGI (`app` stessa) e ASGI (`app.asgi`) per i server di produzione (waitress, gunicorn, uvicorn...), HTTPS con certificato.
  - per il web pubblico: modalita' produzione, proxy fidato, host ammessi, limiti di richieste, file statici con ETag/Range/gzip, registri, /salute.

Sicurezza: per default il server ascolta solo sul tuo computer (127.0.0.1). Con ascolta="0.0.0.0" lo vede tutta la rete.
Per un sito aperto al pubblico: app.configura(produzione=Vero, ...), app.controlla_produzione() e app.avvia_produzione() (waitress) dietro un proxy
HTTPS; PitStudio prepara la cartella per il server (Docker, Caddy, systemd) con «Progetto → Prepara per la pubblicazione».
"""
import ast as _ast
import asyncio as _asincrono
import base64 as _base64
import collections as _collezioni
import copy as _copia
import email.utils as _email_utili
import email.parser as _email_parser
import email.policy as _email_policy
import gzip as _gzip
import hashlib as _hashlib
import hmac as _hmac
import html as _html
import ipaddress as _indirizzi
import inspect as _ispeziona
import json as _json
import logging as _registro_py
import logging.handlers as _registro_gestori
import mimetypes as _mimetypes
import os as _os
import re as _re
import secrets as _segreti
import signal as _segnali
import socketserver as _socketserver
import ssl as _ssl
import sys as _sistema
import threading as _thread
import time as _tempo
import types as _tipi_base
import typing as _tipi
import urllib.parse as _url
import webbrowser as _browser
from http import HTTPStatus as _Stati
from http.cookies import SimpleCookie as _Cookie
from http.server import BaseHTTPRequestHandler as _Gestore, ThreadingHTTPServer as _Server

DIMENSIONE_MASSIMA = 10 * 1024 * 1024        # byte accettati nel corpo di una richiesta (10 MB)
NOME_COOKIE_SESSIONE = "sessione"
INTESTAZIONI_SICUREZZA = {"X-Content-Type-Options": "nosniff", "X-Frame-Options": "SAMEORIGIN", "Referrer-Policy": "same-origin"}
_locale = _thread.local()                    # la richiesta che sta girando in questo filo (serve a @richiede_accesso)


class ErroreWeb(Exception):
    """Da sollevare in una rotta per rispondere con un errore: `solleva ErroreWeb(404, "Non c'e'")`."""

    def __init__(self, stato=500, messaggio="", intestazioni=None):
        Exception.__init__(self, messaggio)
        self.stato = stato
        self.messaggio = messaggio or _frase(stato)
        self.intestazioni = dict(intestazioni or {})          # per esempio {"Retry-After": "30"}


class ErroreValidazione(ErroreWeb):
    """I dati ricevuti non sono validi: risposta 422 con l'elenco dei campi sbagliati."""

    def __init__(self, errori):
        ErroreWeb.__init__(self, 422, "Dati non validi")
        self.errori = errori


def _frase(stato):
    try:
        return _Stati(stato).phrase
    except ValueError:
        return "Errore"


# =====================================================================================================
#  Tipi, conversioni e Modello (validazione dei dati, come pydantic in piccolo)
# =====================================================================================================
_OBBLIGATORIO = object()
_VERO = ("true", "1", "si", "sì", "on", "yes", "vero")
_FALSO = ("false", "0", "no", "off", "falso")


def _nome_tipo(tipo):
    return getattr(tipo, "__name__", None) or str(tipo)


def _converti(valore, tipo, campo, errori, coerce=False, dove="corpo"):
    """Porta `valore` al tipo richiesto. Se non va, aggiunge un errore e ritorna None. coerce=True accetta i testi di un indirizzo o di un modulo ("3" -> 3)."""
    if tipo is _ispeziona.Parameter.empty or tipo is _tipi.Any or tipo is None:
        return valore
    origine = _tipi.get_origin(tipo)
    argomenti = _tipi.get_args(tipo)
    if origine is _tipi.Union or origine is _tipi_base.UnionType:
        if valore is None and type(None) in argomenti:
            return None
        provati = []
        for alternativa in argomenti:
            if alternativa is type(None):
                continue
            prove = []
            risultato = _converti(valore, alternativa, campo, prove, coerce, dove)
            if not prove:
                return risultato
            provati += prove
        errori.extend(provati[:1] or [{"campo": campo, "dove": dove, "messaggio": "valore non valido"}])
        return None
    if origine in (list, _tipi.List):
        if not isinstance(valore, list):
            errori.append({"campo": campo, "dove": dove, "messaggio": "deve essere una lista"})
            return None
        interno = argomenti[0] if argomenti else _tipi.Any
        return [_converti(x, interno, f"{campo}[{i}]", errori, coerce, dove) for i, x in enumerate(valore)]
    if origine is dict or tipo is dict:
        if not isinstance(valore, dict):
            errori.append({"campo": campo, "dove": dove, "messaggio": "deve essere un oggetto (dizionario)"})
            return None
        return valore
    if tipo is list:
        if not isinstance(valore, list):
            errori.append({"campo": campo, "dove": dove, "messaggio": "deve essere una lista"})
            return None
        return valore
    if isinstance(tipo, type) and issubclass(tipo, Modello):
        if isinstance(valore, tipo):
            return valore
        if not isinstance(valore, dict):
            errori.append({"campo": campo, "dove": dove, "messaggio": "deve essere un oggetto"})
            return None
        interni = []
        istanza = tipo._da_dizionario(valore, interni, prefisso=campo + ".", dove=dove)
        errori.extend(interni)
        return istanza
    if tipo is bool:
        if isinstance(valore, bool):
            return valore
        if coerce and isinstance(valore, str):
            if valore.strip().lower() in _VERO:
                return True
            if valore.strip().lower() in _FALSO:
                return False
        errori.append({"campo": campo, "dove": dove, "messaggio": "deve essere vero o falso"})
        return None
    if tipo is int:
        if isinstance(valore, bool):
            errori.append({"campo": campo, "dove": dove, "messaggio": "deve essere un numero intero"})
            return None
        if isinstance(valore, int):
            return valore
        if coerce and isinstance(valore, str) and _re.fullmatch(r"\s*-?\d+\s*", valore):
            return int(valore)
        errori.append({"campo": campo, "dove": dove, "messaggio": "deve essere un numero intero"})
        return None
    if tipo is float:
        if isinstance(valore, bool):
            errori.append({"campo": campo, "dove": dove, "messaggio": "deve essere un numero"})
            return None
        if isinstance(valore, (int, float)):
            return float(valore)
        if coerce and isinstance(valore, str):
            try:
                return float(valore.replace(",", "."))
            except ValueError:
                pass
        errori.append({"campo": campo, "dove": dove, "messaggio": "deve essere un numero"})
        return None
    if tipo is str:
        if isinstance(valore, str):
            return valore
        errori.append({"campo": campo, "dove": dove, "messaggio": "deve essere un testo"})
        return None
    if isinstance(tipo, type):
        if isinstance(valore, tipo):
            return valore
        errori.append({"campo": campo, "dove": dove, "messaggio": f"deve essere di tipo {_nome_tipo(tipo)}"})
        return None
    return valore


class Modello:
    """La forma dei dati che una rotta riceve: i campi con il loro tipo (ed eventualmente un valore predefinito).

        classe Voce(server_web.Modello):
            titolo: tipo_testo
            quantita: tipo_intero = 1
            tag: list = []

        @app.invia("/voci")
        definisci nuova(voce: Voce):          # il JSON ricevuto e' controllato prima di arrivare qui
            ritorna {"titolo": voce.titolo}

    Se un campo manca o ha il tipo sbagliato la risposta e' 422 con l'elenco degli errori. Si puo' usare anche da soli:
    Voce(titolo="pane") oppure Voce.da_dati({"titolo": "pane"}); voce.a_dizionario() torna ai dati."""

    @classmethod
    def campi(cls):
        """{nome: (tipo, valore predefinito o _OBBLIGATORIO)} nell'ordine in cui sono scritti."""
        annotazioni = {}
        for base in reversed(cls.__mro__):
            annotazioni.update({k: v for k, v in getattr(base, "__annotations__", {}).items() if not k.startswith("_")})
        risultato = {}
        for nome, tipo in annotazioni.items():
            risultato[nome] = (tipo, getattr(cls, nome, _OBBLIGATORIO))
        return risultato

    @classmethod
    def _da_dizionario(cls, dati, errori, prefisso="", dove="corpo", coerce=False):
        istanza = cls.__new__(cls)
        for nome, (tipo, predefinito) in cls.campi().items():
            if nome in dati:
                valore = _converti(dati[nome], tipo, prefisso + nome, errori, coerce, dove)
            elif predefinito is not _OBBLIGATORIO:
                valore = _copia.deepcopy(predefinito)
            else:
                errori.append({"campo": prefisso + nome, "dove": dove, "messaggio": "campo obbligatorio"})
                valore = None
            setattr(istanza, nome, valore)
        return istanza

    @classmethod
    def da_dati(cls, dati):
        """Crea il modello da un dizionario; solleva ErroreValidazione se i dati non vanno."""
        errori = []
        istanza = cls._da_dizionario(dati if isinstance(dati, dict) else {}, errori)
        if not isinstance(dati, dict):
            errori = [{"campo": "(corpo)", "dove": "corpo", "messaggio": "deve essere un oggetto JSON"}]
        if errori:
            raise ErroreValidazione(errori)
        return istanza

    def __init__(self, **dati):
        errori = []
        istanza = self._da_dizionario(dati, errori)
        if errori:
            raise ErroreValidazione(errori)
        self.__dict__.update(istanza.__dict__)

    def a_dizionario(self):
        risultato = {}
        for nome in self.campi():
            valore = getattr(self, nome, None)
            risultato[nome] = valore.a_dizionario() if isinstance(valore, Modello) else (
                [x.a_dizionario() if isinstance(x, Modello) else x for x in valore] if isinstance(valore, list) else valore)
        return risultato

    def __repr__(self):
        return f"{type(self).__name__}(" + ", ".join(f"{k}={v!r}" for k, v in self.a_dizionario().items()) + ")"

    def __eq__(self, altro):
        return type(self) is type(altro) and self.a_dizionario() == altro.a_dizionario()


# =====================================================================================================
#  Password
# =====================================================================================================
def cifra_password(password, costo=14):
    """Una password diventa un testo che si puo' salvare nel database (non si puo' tornare alla password). Si controlla con verifica_password."""
    sale = _segreti.token_bytes(16)
    codificato = _base64.b64encode
    try:
        derivata = _hashlib.scrypt(password.encode("utf-8"), salt=sale, n=2 ** costo, r=8, p=1, maxmem=128 * 1024 * 1024, dklen=32)
        return f"scrypt${costo}${codificato(sale).decode()}${codificato(derivata).decode()}"
    except (AttributeError, ValueError):
        derivata = _hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), sale, 600_000, 32)
        return f"pbkdf2${600_000}${codificato(sale).decode()}${codificato(derivata).decode()}"


def verifica_password(password, cifrata):
    """True se la password corrisponde al testo prodotto da cifra_password."""
    try:
        tipo, parametro, sale, atteso = cifrata.split("$")
        sale, atteso = _base64.b64decode(sale), _base64.b64decode(atteso)
        if tipo == "scrypt":
            derivata = _hashlib.scrypt(password.encode("utf-8"), salt=sale, n=2 ** int(parametro), r=8, p=1, maxmem=128 * 1024 * 1024, dklen=len(atteso))
        elif tipo == "pbkdf2":
            derivata = _hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), sale, int(parametro), len(atteso))
        else:
            return False
        return _hmac.compare_digest(derivata, atteso)
    except (ValueError, AttributeError, TypeError):
        return False


# =====================================================================================================
#  Sessione (un dizionario firmato che viaggia in un cookie)
# =====================================================================================================
class Sessione(dict):
    """I dati che il sito ricorda di chi lo sta usando (per esempio chi ha fatto l'accesso). Si usa come un dizionario:
    richiesta.sessione["carrello"] = [1, 2]. Stanno in un cookie firmato: il visitatore non puo' modificarli (ma puo' leggerli)."""

    def __init__(self, *args, **kw):
        dict.__init__(self, *args, **kw)
        self.modificata = False

    def _tocca(nome):
        metodo = getattr(dict, nome)

        def con_segno(self, *a, **k):
            self.modificata = True
            return metodo(self, *a, **k)
        return con_segno
    __setitem__ = _tocca("__setitem__")
    __delitem__ = _tocca("__delitem__")
    pop = _tocca("pop")
    popitem = _tocca("popitem")
    clear = _tocca("clear")
    update = _tocca("update")
    setdefault = _tocca("setdefault")
    del _tocca


def _b64(dati):
    return _base64.urlsafe_b64encode(dati).decode().rstrip("=")


def _unb64(testo):
    return _base64.urlsafe_b64decode(testo + "=" * (-len(testo) % 4))


# =====================================================================================================
#  Richiesta e Risposta
# =====================================================================================================
class FileCaricato:
    """Un file inviato con un modulo (campo <input type="file">): nome_file, tipo, dati (byte), dimensione. salva(cartella) lo scrive su disco."""

    def __init__(self, campo, nome_file, tipo, dati):
        self.campo = campo
        self.nome_file = nome_file
        self.tipo = tipo
        self.dati = dati

    @property
    def dimensione(self):
        return len(self.dati)

    @property
    def testo(self):
        return self.dati.decode("utf-8", "replace")

    def salva(self, cartella, nome=None):
        """Scrive il file in una cartella e ritorna il percorso. Il nome e' ripulito (niente cartelle, niente ..): non puo' uscire dalla cartella."""
        nome = _re.sub(r"[^\w.\- ]", "_", _os.path.basename((nome or self.nome_file or "file").replace("\\", "/"))).strip(". ") or "file"
        _os.makedirs(cartella, exist_ok=True)
        percorso = _os.path.join(cartella, nome)
        with open(percorso, "wb") as f:
            f.write(self.dati)
        return percorso


class Richiesta:
    """Cio' che il browser ha chiesto. Si riceve nelle funzioni di rotta chiedendo un parametro `richiesta`."""

    def __init__(self, metodo, percorso, query, intestazioni, corpo, cliente):
        self.metodo = metodo
        self.percorso = percorso
        self.parametri = {k: v[0] for k, v in query.items()}          # ?a=1&b=2 -> {"a": "1", "b": "2"}
        self.parametri_multipli = query                                # ?a=1&a=2 -> {"a": ["1", "2"]}
        self.intestazioni = intestazioni
        self.corpo = corpo
        self.cliente = cliente                 # l'indirizzo di chi si e' collegato (con un proxy davanti e' quello del proxy)
        self.indirizzo_cliente = cliente       # l'indirizzo vero del visitatore (con proxy_fidato legge X-Forwarded-For)
        self.https = False
        self.id = _segreti.token_hex(6)        # un codice per ritrovare la richiesta nei registri (e nelle pagine d'errore in produzione)
        self.inizio = _tempo.time()
        self._host = None
        self.query_grezza = _url.urlencode(query, doseq=True)
        tipo = (intestazioni.get("Content-Type") or "").split(";")[0].strip().lower()
        self.tipo = tipo
        self._json = None
        self._form = None
        self._file = None
        self._app = None
        self._sessione = None
        cookie = _Cookie()
        try:
            cookie.load(intestazioni.get("Cookie") or "")
        except Exception:
            pass
        self.cookie = {k: m.value for k, m in cookie.items()}

    @property
    def host(self):
        """Il nome del sito richiesto (con proxy_fidato anche X-Forwarded-Host)."""
        return self._host or self.intestazioni.get("Host") or ""

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

    def _leggi_moduli(self):
        if self._form is not None:
            return
        self._form, self._file = {}, {}
        if self.tipo == "application/x-www-form-urlencoded":
            self._form = {k: v[0] for k, v in _url.parse_qs(self.testo, keep_blank_values=True).items()}
        elif self.tipo == "multipart/form-data":
            intestazione = ("Content-Type: " + (self.intestazioni.get("Content-Type") or "") + "\r\nMIME-Version: 1.0\r\n\r\n").encode("latin-1", "replace")
            try:
                messaggio = _email_parser.BytesParser(policy=_email_policy.HTTP).parsebytes(intestazione + self.corpo)
                parti = list(messaggio.iter_parts()) if messaggio.is_multipart() else []
            except Exception:
                raise ErroreWeb(400, "Modulo multipart non valido")
            for parte in parti:
                campo = parte.get_param("name", header="content-disposition")
                if not campo:
                    continue
                nome_file = parte.get_filename()
                dati = parte.get_payload(decode=True) or b""
                if nome_file is not None:
                    self._file[campo] = FileCaricato(campo, nome_file, parte.get_content_type(), dati)
                else:
                    self._form[campo] = dati.decode(parte.get_content_charset() or "utf-8", "replace")

    @property
    def form(self):
        """I campi di un modulo HTML inviato con POST (anche con file): {"nome": "valore"}."""
        self._leggi_moduli()
        return self._form

    @property
    def file(self):
        """I file inviati con un modulo `enctype="multipart/form-data"`: {"campo": FileCaricato}."""
        self._leggi_moduli()
        return self._file

    def valore(self, nome, predefinito=None):
        """Un valore dal form, dal JSON (se e' un dizionario) o dall'indirizzo, in questo ordine."""
        if nome in self.form:
            return self.form[nome]
        dati = self.json if self.tipo == "application/json" else None
        if isinstance(dati, dict) and nome in dati:
            return dati[nome]
        return self.parametri.get(nome, predefinito)

    # ---- sessione, accesso, CSRF
    @property
    def sessione(self):
        """I dati ricordati per questo visitatore (vedi Sessione)."""
        if self._sessione is None:
            self._sessione = self._app._leggi_sessione(self) if self._app is not None else Sessione()
        return self._sessione

    @property
    def utente(self):
        """Chi ha fatto l'accesso (il valore passato ad app.accedi), o Nessuno."""
        return self.sessione.get("utente")

    @property
    def token_csrf(self):
        """Il codice che ogni modulo deve rimandare indietro per dimostrare che viene da una tua pagina (vedi app.configura(csrf=Vero))."""
        if "_csrf" not in self.sessione:
            self.sessione["_csrf"] = _segreti.token_urlsafe(24)
        return self.sessione["_csrf"]

    @property
    def campo_csrf(self):
        """Il campo nascosto da mettere in ogni <form method="post">: {{ campo_csrf }} nei modelli di pagina."""
        return _Sicuro(f'<input type="hidden" name="csrf" value="{_html.escape(self.token_csrf)}">')


class Risposta:
    """Una risposta completa. Di solito basta ritornare un testo o un dizionario: serve per tipo, stato, intestazioni e cookie.
    Risposta.da_file(percorso) invia un file a pezzi (anche grande) con ETag, Last-Modified e richieste parziali (Range)."""

    def __init__(self, corpo="", stato=200, tipo=None, intestazioni=None):
        self.stato = stato
        self.intestazioni = dict(intestazioni or {})
        self.cookie = []
        self._file = None
        self._dimensione_file = 0
        self._intervallo = None
        if isinstance(corpo, (dict, list)):
            corpo = _json.dumps(corpo, ensure_ascii=False)
            tipo = tipo or "application/json; charset=utf-8"
        if isinstance(corpo, str):
            self._corpo = corpo.encode("utf-8")
            tipo = tipo or "text/html; charset=utf-8"
        elif corpo is None:
            self._corpo = b""
        else:
            self._corpo = bytes(corpo)
            tipo = tipo or "application/octet-stream"
        self.tipo = tipo or "text/plain; charset=utf-8"

    @classmethod
    def da_file(cls, percorso, tipo=None, scarica=False, nome=None, cache=None, intestazioni=None):
        """Invia un file. scarica=Vero (o un nome) fa salvare il file invece di mostrarlo. cache: il valore di Cache-Control (es. "public, max-age=3600").
        ATTENZIONE: non passare mai un percorso scelto dall'utente: per i file di una cartella usa app.invia_da_cartella."""
        st = _os.stat(percorso)
        risposta = cls("", 200, tipo or _tipo_file(percorso), intestazioni)
        risposta._corpo = None
        risposta._file = percorso
        risposta._dimensione_file = st.st_size
        risposta.intestazioni["ETag"] = f'W/"{st.st_mtime_ns:x}-{st.st_size:x}"'
        risposta.intestazioni["Last-Modified"] = _email_utili.formatdate(st.st_mtime, usegmt=True)
        risposta.intestazioni["Accept-Ranges"] = "bytes"
        if cache is not None:
            risposta.intestazioni["Cache-Control"] = cache
        if scarica or nome:
            visibile = _os.path.basename((nome or percorso).replace("\\", "/"))
            ascii_ = _re.sub(r"[^A-Za-z0-9._ -]", "_", visibile) or "file"
            risposta.intestazioni["Content-Disposition"] = f"attachment; filename=\"{ascii_}\"; filename*=UTF-8''{_url.quote(visibile)}"
        return risposta

    @property
    def corpo(self):
        """Il corpo come byte (per un file, lo legge tutto: per le prove)."""
        if self._file is not None and self._corpo is None:
            inizio, fine = self._intervallo or (0, self._dimensione_file - 1)
            with open(self._file, "rb") as f:
                f.seek(inizio)
                return f.read(fine - inizio + 1)
        return self._corpo

    @corpo.setter
    def corpo(self, valore):
        self._corpo = valore

    @property
    def in_flusso(self):
        return self._file is not None

    @property
    def lunghezza(self):
        """Quanti byte verranno inviati."""
        if self._file is not None:
            if self._intervallo:
                return self._intervallo[1] - self._intervallo[0] + 1
            return self._dimensione_file
        return len(self._corpo)

    def blocchi(self, dimensione=65536):
        """Il corpo a pezzi (un file non viene mai letto tutto in memoria)."""
        if self._file is None:
            if self._corpo:
                yield self._corpo
            return
        inizio, fine = self._intervallo or (0, self._dimensione_file - 1)
        with open(self._file, "rb") as f:
            f.seek(inizio)
            restante = fine - inizio + 1
            while restante > 0:
                pezzo = f.read(min(dimensione, restante))
                if not pezzo:
                    break
                restante -= len(pezzo)
                yield pezzo

    @property
    def testo(self):
        """Il corpo della risposta come testo."""
        return self.corpo.decode("utf-8", "replace")

    @property
    def dati(self):
        """Il corpo della risposta letto come JSON (utile per provare le API)."""
        return _json.loads(self.testo)

    @property
    def cookie_impostati(self):
        """I cookie che la risposta chiede di ricordare: {nome: valore}."""
        risultato = {}
        for c in self.cookie:
            nome, _, resto = c.partition("=")
            risultato[nome] = resto.split(";")[0]
        return risultato

    def imposta_cookie(self, nome, valore, durata=None, percorso="/", solo_http=True, sicuro=False):
        """Chiede al browser di ricordare un cookie. durata: secondi (Nessuno = finche' il browser resta aperto)."""
        c = _Cookie()
        c[nome] = valore
        c[nome]["path"] = percorso
        if durata is not None:
            c[nome]["max-age"] = int(durata)
        if solo_http:
            c[nome]["httponly"] = True
        if sicuro:
            c[nome]["secure"] = True
        c[nome]["samesite"] = "Lax"
        self.cookie.append(c[nome].OutputString())
        return self

    def togli_cookie(self, nome, percorso="/"):
        return self.imposta_cookie(nome, "", durata=0, percorso=percorso)


def invia_file(percorso, nome=None, scarica=False, tipo=None, cache=None):
    """Una risposta con un file (a pezzi, con ETag e Range). ATTENZIONE: il percorso lo scegli tu, non l'utente (vedi app.invia_da_cartella)."""
    return Risposta.da_file(percorso, tipo=tipo, scarica=scarica, nome=nome, cache=cache)


def reindirizza(indirizzo, stato=302):
    """Manda il browser a un'altra pagina: `ritorna reindirizza("/grazie")`."""
    return Risposta("", stato, intestazioni={"Location": indirizzo})


def json_risposta(dati, stato=200):
    """Una risposta JSON con lo stato che scegli: `ritorna json_risposta({"errore": "manca il nome"}, 400)`."""
    return Risposta(dati, stato)


# =====================================================================================================
#  Modelli di pagina (un piccolo motore con cicli, condizioni, inclusioni ed ereditarieta')
# =====================================================================================================
class _Sicuro(str):
    """Un testo gia' pronto per l'HTML: non va reso innocuo una seconda volta."""


class _Mancante:
    """Una variabile che non esiste: nella pagina diventa un testo vuoto, e non da errore se ci si chiede qualcosa."""

    def __bool__(self):
        return False

    def __str__(self):
        return ""

    def __iter__(self):
        return iter(())

    def __getattr__(self, nome):
        return self

    def __getitem__(self, chiave):
        return self

    def __call__(self, *a, **k):
        return self

    def __len__(self):
        return 0


_MANCANTE = _Mancante()
_PAROLE_ESPRESSIONE = {"e": "and", "o": "or", "non": "not", "è": "is", "Vero": "True", "Falso": "False", "Nessuno": "None"}
_METODI_AMMESSI = {"items", "keys", "values", "lower", "upper", "title", "strip", "capitalize", "startswith", "endswith", "get", "count"}
_FUNZIONI_AMMESSE = {"lunghezza_di": len, "len": len, "intervallo_di": range, "range": range, "tipo_testo": str, "tipo_intero": int, "minimo": min,
                     "massimo": max, "min": min, "max": max, "arrotonda": round, "round": round}


def _filtro_json(valore, *a):
    testo = _json.dumps(valore, ensure_ascii=False).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    return _Sicuro(testo)


def _filtro_data(valore, formato="%d/%m/%Y"):
    if isinstance(valore, (int, float)):
        return _tempo.strftime(formato, _tempo.localtime(valore))
    try:
        return valore.strftime(formato)
    except AttributeError:
        return str(valore)


_FILTRI = {
    "grezzo": lambda v: _Sicuro("" if v is None or v is _MANCANTE else str(v)),
    "maiuscolo": lambda v: str(v).upper(), "minuscolo": lambda v: str(v).lower(), "titolo": lambda v: str(v).title(),
    "lunghezza": lambda v: len(v), "json": _filtro_json,
    "predefinito": lambda v, d="": d if (v is None or v is _MANCANTE or v == "") else v,
    "tronca": lambda v, n=50: (str(v) if len(str(v)) <= n else str(v)[:max(0, n - 1)] + "…"),
    "data": _filtro_data, "arrotonda": lambda v, n=0: round(v, n), "ordina": lambda v: sorted(v), "inverti": lambda v: list(reversed(v)),
    "unisci": lambda v, s=", ": s.join(str(x) for x in v), "primo": lambda v: v[0] if v else _MANCANTE,
    "ultimo": lambda v: v[-1] if v else _MANCANTE,
}


def _prepara_espressione(testo):
    """Traduce le parole italiane (e, o, non, e', Vero...) di un'espressione in Python, lasciando stare i testi tra virgolette."""
    pezzi = _re.split(r"""("(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')""", testo)
    for i in range(0, len(pezzi), 2):
        pezzi[i] = _re.sub(r"[^\W\d]\w*", lambda m: _PAROLE_ESPRESSIONE.get(m.group(0), m.group(0)), pezzi[i])
    return "".join(pezzi)


def _compila_espressione(testo, nome="espressione"):
    try:
        albero = _ast.parse(_prepara_espressione(testo.strip()), mode="eval")
    except SyntaxError:
        raise ErroreModello(f"espressione non valida nel modello «{nome}»: {testo.strip()!r}")
    for nodo in _ast.walk(albero):
        if not isinstance(nodo, (_ast.Expression, _ast.BoolOp, _ast.And, _ast.Or, _ast.UnaryOp, _ast.Not, _ast.USub, _ast.UAdd, _ast.BinOp, _ast.Add,
                                 _ast.Sub, _ast.Mult, _ast.Div, _ast.Mod, _ast.FloorDiv, _ast.Compare, _ast.Eq, _ast.NotEq, _ast.Lt, _ast.LtE, _ast.Gt,
                                 _ast.GtE, _ast.In, _ast.NotIn, _ast.Is, _ast.IsNot, _ast.Name, _ast.Load, _ast.Constant, _ast.Attribute, _ast.Subscript,
                                 _ast.Tuple, _ast.List, _ast.Dict, _ast.IfExp, _ast.Call, _ast.Slice)):
            raise ErroreModello(f"nel modello «{nome}» l'espressione {testo.strip()!r} usa qualcosa che non e' permesso ({type(nodo).__name__})")
    return albero.body


class ErroreModello(Exception):
    """Un errore nella scrittura di un modello di pagina."""


def _valuta(nodo, ctx):
    t = type(nodo)
    if t is _ast.Constant:
        return nodo.value
    if t is _ast.Name:
        if nodo.id in ctx:
            return ctx[nodo.id]
        return _MANCANTE
    if t is _ast.Attribute:
        base = _valuta(nodo.value, ctx)
        if nodo.attr.startswith("_"):
            return _MANCANTE
        if isinstance(base, dict) and nodo.attr in base:
            return base[nodo.attr]
        if isinstance(base, Sessione) or isinstance(base, dict):
            return getattr(base, nodo.attr, _MANCANTE) if nodo.attr in _METODI_AMMESSI else _MANCANTE
        return getattr(base, nodo.attr, _MANCANTE)
    if t is _ast.Subscript:
        base = _valuta(nodo.value, ctx)
        try:
            return base[_valuta(nodo.slice, ctx)]
        except (KeyError, IndexError, TypeError):
            return _MANCANTE
    if t is _ast.Slice:
        return slice(_valuta(nodo.lower, ctx) if nodo.lower else None, _valuta(nodo.upper, ctx) if nodo.upper else None,
                     _valuta(nodo.step, ctx) if nodo.step else None)
    if t is _ast.BoolOp:
        if isinstance(nodo.op, _ast.And):
            risultato = True
            for v in nodo.values:
                risultato = _valuta(v, ctx)
                if not risultato:
                    return risultato
            return risultato
        risultato = False
        for v in nodo.values:
            risultato = _valuta(v, ctx)
            if risultato:
                return risultato
        return risultato
    if t is _ast.UnaryOp:
        v = _valuta(nodo.operand, ctx)
        return {_ast.Not: lambda x: not x, _ast.USub: lambda x: -x, _ast.UAdd: lambda x: +x}[type(nodo.op)](v)
    if t is _ast.BinOp:
        a, b = _valuta(nodo.left, ctx), _valuta(nodo.right, ctx)
        try:
            return {_ast.Add: lambda: a + b, _ast.Sub: lambda: a - b, _ast.Mult: lambda: a * b, _ast.Div: lambda: a / b, _ast.Mod: lambda: a % b,
                    _ast.FloorDiv: lambda: a // b}[type(nodo.op)]()
        except (TypeError, ZeroDivisionError):
            return _MANCANTE
    if t is _ast.Compare:
        sinistra = _valuta(nodo.left, ctx)
        for operatore, destro in zip(nodo.ops, nodo.comparators):
            destra = _valuta(destro, ctx)
            try:
                ok = {_ast.Eq: lambda: sinistra == destra, _ast.NotEq: lambda: sinistra != destra, _ast.Lt: lambda: sinistra < destra,
                      _ast.LtE: lambda: sinistra <= destra, _ast.Gt: lambda: sinistra > destra, _ast.GtE: lambda: sinistra >= destra,
                      _ast.In: lambda: sinistra in destra, _ast.NotIn: lambda: sinistra not in destra, _ast.Is: lambda: sinistra is destra,
                      _ast.IsNot: lambda: sinistra is not destra}[type(operatore)]()
            except TypeError:
                ok = False
            if not ok:
                return False
            sinistra = destra
        return True
    if t is _ast.IfExp:
        return _valuta(nodo.body, ctx) if _valuta(nodo.test, ctx) else _valuta(nodo.orelse, ctx)
    if t is _ast.Tuple or t is _ast.List:
        return [_valuta(x, ctx) for x in nodo.elts] if t is _ast.List else tuple(_valuta(x, ctx) for x in nodo.elts)
    if t is _ast.Dict:
        return {_valuta(k, ctx): _valuta(v, ctx) for k, v in zip(nodo.keys, nodo.values)}
    if t is _ast.Call:
        if nodo.keywords:
            raise ErroreModello("nei modelli le chiamate non accettano argomenti con nome")
        argomenti = [_valuta(a, ctx) for a in nodo.args]
        if isinstance(nodo.func, _ast.Name) and nodo.func.id in _FUNZIONI_AMMESSE:
            return _FUNZIONI_AMMESSE[nodo.func.id](*argomenti)
        if isinstance(nodo.func, _ast.Attribute) and nodo.func.attr in _METODI_AMMESSI:
            return getattr(_valuta(nodo.func.value, ctx), nodo.func.attr)(*argomenti)
        raise ErroreModello("nei modelli si possono chiamare solo " + ", ".join(sorted(_FUNZIONI_AMMESSE)) + " e i metodi " + ", ".join(sorted(_METODI_AMMESSI)))
    raise ErroreModello("espressione non permessa nel modello")


def _spezza_filtri(testo):
    """«x|maiuscolo|tronca(5)» -> ["x", "maiuscolo", "tronca(5)"] (il | dentro testi e parentesi non conta)."""
    pezzi, corrente, profondita, virgolette = [], "", 0, None
    for c in testo:
        if virgolette:
            corrente += c
            if c == virgolette:
                virgolette = None
        elif c in "\"'":
            virgolette = c
            corrente += c
        elif c in "([{":
            profondita += 1
            corrente += c
        elif c in ")]}":
            profondita -= 1
            corrente += c
        elif c == "|" and profondita == 0:
            pezzi.append(corrente)
            corrente = ""
        else:
            corrente += c
    pezzi.append(corrente)
    return [p.strip() for p in pezzi]


class _Variabile:
    def __init__(self, testo, nome):
        pezzi = _spezza_filtri(testo)
        self.espressione = _compila_espressione(pezzi[0], nome)
        self.filtri = []
        for f in pezzi[1:]:
            m = _re.fullmatch(r"(\w+)(?:\((.*)\))?", f, _re.S)
            if not m or m.group(1) not in _FILTRI:
                raise ErroreModello(f"nel modello «{nome}» il filtro {f!r} non esiste (ci sono: {', '.join(sorted(_FILTRI))})")
            argomenti = _compila_espressione("[" + m.group(2) + "]", nome) if m.group(2) else None
            self.filtri.append((_FILTRI[m.group(1)], argomenti))

    def rendi(self, ctx):
        valore = _valuta(self.espressione, ctx)
        for funzione, argomenti in self.filtri:
            valore = funzione(valore, *(_valuta(argomenti, ctx) if argomenti else []))
        if isinstance(valore, _Sicuro):
            return str(valore)
        if valore is None or valore is _MANCANTE:
            return ""
        return _html.escape(str(valore))


_TOKEN = _re.compile(r"(\{%.*?%\}|\{\{.*?\}\}|\{#.*?#\})", _re.S)


class _Modello:
    """Un modello di pagina compilato."""

    def __init__(self, testo, nome="pagina", cartella=None, motore=None):
        self.nome = nome
        self.motore = motore
        self.cartella = cartella
        self.padre = None
        self.blocchi = {}
        pezzi = [p for p in _TOKEN.split(testo)]
        self.nodi, _fine = self._analizza(pezzi, 0, ())

    def _analizza(self, pezzi, i, terminatori):
        nodi = []
        while i < len(pezzi):
            p = pezzi[i]
            if p.startswith("{#"):
                i += 1
            elif p.startswith("{{"):
                nodi.append(("var", _Variabile(p[2:-2], self.nome)))
                i += 1
            elif p.startswith("{%"):
                istruzione = p[2:-2].strip()
                parola = istruzione.split(None, 1)[0] if istruzione else ""
                resto = istruzione[len(parola):].strip()
                if parola in terminatori:
                    return nodi, (i, parola, resto)
                if parola == "se":
                    rami, altro = [], None
                    condizione = _compila_espressione(resto, self.nome)
                    corpo, fine = self._analizza(pezzi, i + 1, ("altrimenti_se", "altrimenti", "fine"))
                    rami.append((condizione, corpo))
                    while fine and fine[1] != "fine":
                        if fine[1] == "altrimenti_se":
                            condizione = _compila_espressione(fine[2], self.nome)
                            corpo, fine = self._analizza(pezzi, fine[0] + 1, ("altrimenti_se", "altrimenti", "fine"))
                            rami.append((condizione, corpo))
                        else:
                            altro, fine = self._analizza(pezzi, fine[0] + 1, ("fine",))
                    if not fine:
                        raise ErroreModello(f"nel modello «{self.nome}» manca {{% fine %}} dopo un «se»")
                    nodi.append(("se", rami, altro))
                    i = fine[0] + 1
                elif parola == "per":
                    m = _re.fullmatch(r"(.+?)\s+in\s+(.+)", resto, _re.S)
                    if not m:
                        raise ErroreModello(f"nel modello «{self.nome}» il «per» va scritto cosi': per x in elenco")
                    variabili = [v.strip() for v in m.group(1).split(",")]
                    corpo, fine = self._analizza(pezzi, i + 1, ("altrimenti", "fine"))
                    altro = None
                    if fine and fine[1] == "altrimenti":
                        altro, fine = self._analizza(pezzi, fine[0] + 1, ("fine",))
                    if not fine:
                        raise ErroreModello(f"nel modello «{self.nome}» manca {{% fine %}} dopo un «per»")
                    nodi.append(("per", variabili, _compila_espressione(m.group(2), self.nome), corpo, altro))
                    i = fine[0] + 1
                elif parola == "includi":
                    nodi.append(("includi", _compila_espressione(resto, self.nome)))
                    i += 1
                elif parola == "estende":
                    self.padre = _compila_espressione(resto, self.nome)
                    i += 1
                elif parola == "blocco":
                    corpo, fine = self._analizza(pezzi, i + 1, ("fine",))
                    if not fine:
                        raise ErroreModello(f"nel modello «{self.nome}» manca {{% fine %}} dopo un «blocco»")
                    self.blocchi[resto] = corpo
                    nodi.append(("blocco", resto))
                    i = fine[0] + 1
                else:
                    raise ErroreModello(f"nel modello «{self.nome}» l'istruzione {{% {istruzione} %}} non esiste (ci sono: se, per, includi, estende, blocco, fine)")
            else:
                if p:
                    nodi.append(("testo", p))
                i += 1
        if terminatori:
            return nodi, None
        return nodi, None

    def rendi(self, ctx, blocchi_figli=None):
        if self.padre is not None:
            nome_padre = _valuta(self.padre, ctx)
            if not self.motore:
                raise ErroreModello("«estende» si puo' usare solo con app.mostra o carica_pagina")
            blocchi = dict(blocchi_figli or {})
            for k, v in self.blocchi.items():
                blocchi.setdefault(k, (self, v))
            return self.motore.carica(str(nome_padre), self.cartella).rendi(ctx, blocchi)
        out = []
        self._rendi_nodi(self.nodi, ctx, out, blocchi_figli or {})
        return "".join(out)

    def _rendi_nodi(self, nodi, ctx, out, blocchi):
        for n in nodi:
            tipo = n[0]
            if tipo == "testo":
                out.append(n[1])
            elif tipo == "var":
                out.append(n[1].rendi(ctx))
            elif tipo == "se":
                for condizione, corpo in n[1]:
                    if _valuta(condizione, ctx):
                        self._rendi_nodi(corpo, ctx, out, blocchi)
                        break
                else:
                    if n[2] is not None:
                        self._rendi_nodi(n[2], ctx, out, blocchi)
            elif tipo == "per":
                _, variabili, elenco, corpo, altro = n
                valori = _valuta(elenco, ctx)
                if isinstance(valori, dict):
                    valori = list(valori)
                try:
                    valori = list(valori)
                except TypeError:
                    valori = []
                if not valori and altro is not None:
                    self._rendi_nodi(altro, ctx, out, blocchi)
                for indice, v in enumerate(valori):
                    figlio = dict(ctx)
                    if len(variabili) == 1:
                        figlio[variabili[0]] = v
                    else:
                        try:
                            for nome, x in zip(variabili, v):
                                figlio[nome] = x
                        except TypeError:
                            pass
                    figlio["ciclo"] = {"indice": indice + 1, "indice0": indice, "primo": indice == 0, "ultimo": indice == len(valori) - 1, "totale": len(valori)}
                    self._rendi_nodi(corpo, figlio, out, blocchi)
            elif tipo == "includi":
                if not self.motore:
                    raise ErroreModello("«includi» si puo' usare solo con app.mostra o carica_pagina")
                out.append(self.motore.carica(str(_valuta(n[1], ctx)), self.cartella).rendi(ctx))
            elif tipo == "blocco":
                proprietario, corpo = blocchi.get(n[1], (self, self.blocchi[n[1]]))
                proprietario._rendi_nodi(corpo, ctx, out, blocchi)


class _Motore:
    """Legge i modelli di pagina da una cartella e li tiene pronti (si ricaricano da soli se il file cambia)."""

    def __init__(self):
        self._cache = {}

    def carica(self, nome, cartella):
        if not cartella:
            raise ErroreModello("per «includi» e «estende» serve una cartella di pagine (app.configura(cartella_pagine=...))")
        base = _os.path.abspath(cartella)
        percorso = _os.path.abspath(_os.path.join(base, nome))
        if percorso != base and not percorso.startswith(base + _os.sep):
            raise ErroreModello(f"il modello {nome!r} e' fuori dalla cartella delle pagine")
        try:
            data = _os.path.getmtime(percorso)
        except OSError:
            raise ErroreModello(f"modello di pagina non trovato: {nome}")
        voce = self._cache.get(percorso)
        if voce is None or voce[0] != data:
            with open(percorso, encoding="utf-8") as f:
                modello = _Modello(f.read(), nome, base, self)
            self._cache[percorso] = (data, modello)
            voce = self._cache[percorso]
        return voce[1]


_motore = _Motore()


def pagina(modello, /, **valori):
    """Riempie un modello di pagina: {{ nome }} (reso innocuo: < > & " non diventano codice), {{ nome|grezzo }} (cosi' com'e'),
    {% se condizione %}...{% altrimenti %}...{% fine %}, {% per x in elenco %}...{% fine %}, filtri come |maiuscolo, |tronca(20), |predefinito("n/d").
    Una variabile che manca resta vuota. Per «includi» e «estende» usa app.mostra o carica_pagina."""
    return _Modello(modello, "pagina", None, None).rendi(dict(valori))


def carica_pagina(file, /, **valori):
    """Legge un file HTML (anche con {% estende %} e {% includi %} nella stessa cartella) e lo riempie come pagina()."""
    percorso = _os.path.abspath(file)
    return _motore.carica(_os.path.basename(percorso), _os.path.dirname(percorso)).rendi(dict(valori))


# =====================================================================================================
#  Rotte
# =====================================================================================================
_TIPI_PARAMETRO = ("testo", "str", "numero", "int", "resto", "path")


class _Rotta:
    def __init__(self, modello, metodi, funzione):
        modello = _re.sub(r"\{(\w+)(?::(\w+))?\}", lambda m: "<" + m.group(1) + (":" + m.group(2) if m.group(2) else "") + ">", modello)    # anche alla maniera di FastAPI: /voci/{id}
        self.modello = modello
        self.metodi = tuple(m.upper() for m in metodi)
        self.funzione = funzione
        self.tipi = {}
        self.nomi_url = []
        pezzi = []
        for parte in _re.split(r"(<[^<>]+>)", modello):
            m = _re.fullmatch(r"<(\w+)(?::(\w+))?>", parte) if parte.startswith("<") else None
            if not m:
                pezzi.append(_re.escape(parte))
                continue
            nome, tipo = m.group(1), m.group(2) or "testo"
            if nome in _TIPI_PARAMETRO and tipo not in _TIPI_PARAMETRO:        # anche alla maniera di Flask: <int:n>
                nome, tipo = tipo, nome
            self.nomi_url.append(nome)
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
        self.firma = _ispeziona.signature(funzione)
        try:
            self.suggerimenti = _tipi.get_type_hints(funzione)
        except Exception:
            self.suggerimenti = {k: p.annotation for k, p in self.firma.parameters.items() if p.annotation is not _ispeziona.Parameter.empty}
        self.nomi = set(self.firma.parameters)
        self.accetta_tutto = any(p.kind is p.VAR_KEYWORD for p in self.firma.parameters.values())
        self.senza_csrf = bool(getattr(funzione, "_senza_csrf", False))
        self.nascosta = False

    def corrisponde(self, percorso):
        m = self.regola.fullmatch(percorso)
        if not m:
            return None
        valori = {k: _url.unquote(v) for k, v in m.groupdict().items()}
        for nome, tipo in self.tipi.items():
            valori[nome] = tipo(valori[nome])
        return valori

    def parametri_della_funzione(self):
        """Per ogni parametro della funzione: (nome, dove, tipo, predefinito). dove: indirizzo, richiesta, corpo, query."""
        risultato = []
        for nome, p in self.firma.parameters.items():
            if p.kind in (p.VAR_KEYWORD, p.VAR_POSITIONAL):
                continue
            tipo = self.suggerimenti.get(nome, _ispeziona.Parameter.empty)
            predefinito = _OBBLIGATORIO if p.default is p.empty else p.default
            if nome == "richiesta":
                dove = "richiesta"
            elif nome in self.nomi_url:
                dove = "indirizzo"
            elif (isinstance(tipo, type) and issubclass(tipo, Modello)) or nome == "corpo":
                dove = "corpo"
            else:
                dove = "query"
            risultato.append((nome, dove, tipo, predefinito))
        return risultato

    def associa(self, richiesta, valori_url):
        """Prepara gli argomenti della funzione: indirizzo, richiesta, corpo JSON e parametri dell'indirizzo, con tipi controllati."""
        argomenti, errori = {}, []
        if self.accetta_tutto:
            argomenti.update(valori_url)
            argomenti["richiesta"] = richiesta
        for nome, dove, tipo, predefinito in self.parametri_della_funzione():
            if dove == "richiesta":
                argomenti[nome] = richiesta
            elif dove == "indirizzo":
                valore = valori_url.get(nome)
                if tipo is _ispeziona.Parameter.empty or (nome in self.tipi and tipo is int):
                    argomenti[nome] = valore
                else:
                    argomenti[nome] = _converti(valore, tipo, nome, errori, coerce=True, dove="indirizzo")
            elif dove == "corpo":
                dati = richiesta.json
                if dati is None:
                    if predefinito is not _OBBLIGATORIO:
                        argomenti[nome] = predefinito
                    else:
                        errori.append({"campo": nome, "dove": "corpo", "messaggio": "manca il corpo JSON della richiesta"})
                elif tipo is _ispeziona.Parameter.empty or nome == "corpo" and not (isinstance(tipo, type) and issubclass(tipo, Modello)):
                    argomenti[nome] = dati
                else:
                    interni = []
                    argomenti[nome] = _converti(dati, tipo, nome, interni, dove="corpo")
                    errori.extend({**e, "campo": e["campo"][len(nome) + 1:] if e["campo"].startswith(nome + ".") else e["campo"]} for e in interni)
            else:
                multiplo = _tipi.get_origin(tipo) in (list, _tipi.List) or tipo is list
                if nome in richiesta.parametri:
                    valore = richiesta.parametri_multipli[nome] if multiplo else richiesta.parametri[nome]
                    if multiplo:
                        interno = _tipi.get_args(tipo)[0] if _tipi.get_args(tipo) else str
                        argomenti[nome] = [_converti(x, interno, nome, errori, coerce=True, dove="query") for x in valore]
                    else:
                        argomenti[nome] = _converti(valore, tipo, nome, errori, coerce=True, dove="query")
                elif predefinito is not _OBBLIGATORIO:
                    argomenti[nome] = predefinito
                elif nome in valori_url:
                    argomenti[nome] = valori_url[nome]
                else:
                    errori.append({"campo": nome, "dove": "query", "messaggio": "obbligatorio (si scrive nell'indirizzo: ?" + nome + "=...)"})
        if errori:
            raise ErroreValidazione(errori)
        return argomenti


class Gruppo:
    """Rotte che condividono un prefisso: `api = app.gruppo("/api")` e poi `@api.rotta("/voci")` risponde a /api/voci.
    Un Gruppo creato da solo (Gruppo("/api")) si collega con app.registra(gruppo)."""

    def __init__(self, prefisso="", app=None):
        self.prefisso = prefisso.rstrip("/")
        self._app = app
        self._voci = []

    def rotta(self, percorso, metodi=("GET",)):
        if not percorso.startswith("/"):
            raise ValueError(f"l'indirizzo deve cominciare con / (invece e' {percorso!r})")

        def registra(funzione):
            self._voci.append((percorso, tuple(metodi), funzione))
            if self._app is not None:
                self._app._aggiungi(self.prefisso + percorso, metodi, funzione)
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

    def registra(self, altro, prefisso=""):
        """Aggiunge a questo gruppo le rotte di un altro (con un prefisso in piu')."""
        for percorso, metodi, funzione in altro._voci:
            self._voci.append((prefisso.rstrip("/") + altro.prefisso + percorso, metodi, funzione))
            if self._app is not None:
                self._app._aggiungi(self.prefisso + prefisso.rstrip("/") + altro.prefisso + percorso, metodi, funzione)


def _tipo_file(percorso):
    tipo = _mimetypes.guess_type(percorso)[0] or "application/octet-stream"
    return tipo + ("; charset=utf-8" if tipo.startswith("text/") or tipo in ("application/javascript", "application/json") else "")


class ErroreProduzione(Exception):
    """Il sito non e' pronto per la produzione (o manca waitress): il messaggio dice cosa fare."""


class _Limitatore:
    """Conta le richieste recenti per chiave (finestra scorrevole). Sta in memoria e funziona con piu' fili."""

    def __init__(self):
        self._voci = {}
        self._blocco = _thread.Lock()

    def colpisci(self, chiave, massimo, secondi):
        """(ammessa, secondi da attendere). Registra la richiesta solo se e' ammessa."""
        ora = _tempo.monotonic()
        with self._blocco:
            voce = self._voci.get(chiave)
            if voce is None:
                voce = self._voci[chiave] = (_collezioni.deque(), secondi)
            coda = voce[0]
            while coda and coda[0] <= ora - secondi:
                coda.popleft()
            if len(coda) >= massimo:
                return False, max(1, int(coda[0] + secondi - ora) + 1)
            coda.append(ora)
            if len(self._voci) > 20000:
                self._voci = {k: v for k, v in self._voci.items() if v[0] and v[0][-1] > ora - v[1]}
            return True, 0


class _ServerRobusto(_Server):
    """Il server integrato con un limite alle connessioni contemporanee: oltre il limite risponde 503 subito invece di creare fili all'infinito."""
    request_queue_size = 128

    def __init__(self, indirizzo, gestore, massimo):
        self._limite_connessioni = _thread.BoundedSemaphore(max(1, massimo))
        _Server.__init__(self, indirizzo, gestore)

    def process_request(self, richiesta, indirizzo_cliente):
        if not self._limite_connessioni.acquire(blocking=False):
            try:
                richiesta.settimeout(0.3)
                try:
                    richiesta.recv(65536)               # si legge la richiesta (e si scarta): chiudere con dati non letti farebbe perdere la risposta al client
                except OSError:
                    pass
                richiesta.sendall(b"HTTP/1.1 503 Service Unavailable\r\nRetry-After: 1\r\nContent-Length: 0\r\nConnection: close\r\n\r\n")
            except OSError:
                pass
            self.shutdown_request(richiesta)
            return
        try:
            _Server.process_request(self, richiesta, indirizzo_cliente)
        except BaseException:
            self._limite_connessioni.release()
            raise

    def process_request_thread(self, richiesta, indirizzo_cliente):
        try:
            _Server.process_request_thread(self, richiesta, indirizzo_cliente)
        finally:
            self._limite_connessioni.release()


MAX_RICHIESTE_PER_CONNESSIONE = 100


# =====================================================================================================
#  L'applicazione
# =====================================================================================================
class Applicazione(Gruppo):
    """Il tuo sito: registra le rotte e poi `avvia()`.

    registro: Vero (predefinito) scrive una riga per ogni richiesta («GET /pagina 200»), cosi' la console di PitStudio la mostra.
    Regolazioni (app.configura): chiave_segreta, durata_sessione, csrf, cartella_pagine, dimensione_massima, cookie_sicuro, intestazioni_sicurezza."""

    def __init__(self, nome="app", registro=True):
        Gruppo.__init__(self, "", None)
        self.nome = nome
        self.registro = registro
        self._rotte = []
        self._statici = []
        self._gestori_errore = {}
        self._prima = []
        self._dopo = []
        self._all_avvio = []
        self._alla_chiusura = []
        self.dati = {}                         # un posto dove tenere cio' che serve a piu' rotte (per esempio la connessione al database)
        self._chiave = _segreti.token_bytes(32)
        self._chiave_temporanea = True
        self.durata_sessione = 14 * 24 * 3600
        self.csrf = False
        self.cartella_pagine = None
        self.dimensione_massima = None
        self.cookie_sicuro = False
        self.intestazioni_sicurezza = dict(INTESTAZIONI_SICUREZZA)
        self._https = False
        self._documentazione = None
        self._app = self
        # ---- per il web pubblico
        self.produzione = False
        self.proxy_fidato = False
        self._proxy_reti = None
        self._proxy_numero = 1
        self.host_ammessi = []
        self.forza_https = False
        self.hsts = None
        self.csp = None
        self._cors = None
        self.compressione = True
        self.cache_statici = None
        self.registro_file = None
        self.registro_errori = None
        self._log_accessi = None
        self._log_errori = None
        self.limite_globale = None
        self.limite_accessi = (5, 900, 900)
        self.timeout_connessione = 30
        self.connessioni_massime = 200
        self._limiti = _Limitatore()
        self._tentativi = {}
        self._blocco_tentativi = _thread.Lock()
        self._esenti = set()
        self._avvio_tempo = _tempo.time()
        self._ascolta = None

    # ---- regolazioni
    def configura(self, chiave_segreta=None, durata_sessione=None, csrf=None, cartella_pagine=None, dimensione_massima=None, cookie_sicuro=None,
                  intestazioni_sicurezza=None, produzione=None, proxy_fidato=None, host_ammessi=None, forza_https=None, hsts=None, csp=None,
                  compressione=None, cache_statici=None, registro_file=None, registro_errori=None, limite_globale=None, limite_accessi=None,
                  timeout_connessione=None, connessioni_massime=None):
        """Le regolazioni del sito, tutte facoltative.

        Sessioni e moduli:
          chiave_segreta: il testo con cui si firmano i cookie di sessione (tienilo riservato; senza, le sessioni durano finche' il server resta acceso);
          durata_sessione: secondi (predefinito: 14 giorni);  csrf=Vero: ogni modulo (POST...) deve rimandare il codice di richiesta.token_csrf;
          cartella_pagine: dove sono i modelli di pagina per app.mostra;  dimensione_massima: byte accettati in una richiesta;
          cookie_sicuro=Vero: i cookie viaggiano solo su HTTPS;  intestazioni_sicurezza: dizionario che sostituisce quelle predefinite.
        Per il web pubblico (vedi la guida «Pubblicare un sito»):
          produzione=Vero: gli errori non mostrano dettagli ma un codice, /docs resta spenta, gli statici si ricordano un'ora;
          proxy_fidato: Vero (c'e' un proxy davanti), un numero di proxy, o un elenco di reti ["10.0.0.0/8"]: legge X-Forwarded-For/Proto/Host;
          host_ammessi: i nomi con cui il sito puo' essere chiamato, ["esempio.it", "*.esempio.it"] (obbligatorio con forza_https);
          forza_https=Vero: chi arriva in HTTP viene mandato a HTTPS;  hsts: secondi di Strict-Transport-Security (predefinito un anno su HTTPS in produzione);
          csp: il valore di Content-Security-Policy;  compressione=Falso: niente gzip;  cache_statici: secondi di cache dei file statici;
          registro_file / registro_errori: file dei registri (con rotazione);  limite_globale=(richieste, secondi): massimo per indirizzo IP;
          limite_accessi=(tentativi, finestra, blocco): vedi app.accesso_fallito;  timeout_connessione e connessioni_massime: per il server integrato."""
        if chiave_segreta is not None:
            if len(chiave_segreta) < 16:
                raise ValueError("la chiave segreta deve avere almeno 16 caratteri (meglio 32 o piu')")
            self._chiave = chiave_segreta.encode("utf-8") if isinstance(chiave_segreta, str) else bytes(chiave_segreta)
            self._chiave_temporanea = False
        if durata_sessione is not None:
            self.durata_sessione = int(durata_sessione)
        if csrf is not None:
            self.csrf = bool(csrf)
        if cartella_pagine is not None:
            self.cartella_pagine = cartella_pagine
        if dimensione_massima is not None:
            self.dimensione_massima = int(dimensione_massima)
        if cookie_sicuro is not None:
            self.cookie_sicuro = bool(cookie_sicuro)
        if intestazioni_sicurezza is not None:
            self.intestazioni_sicurezza = dict(intestazioni_sicurezza)
        if produzione is not None:
            self.produzione = bool(produzione)
        if proxy_fidato is not None:
            self._imposta_proxy(proxy_fidato)
        if host_ammessi is not None:
            self.host_ammessi = [h.strip().lower() for h in ([host_ammessi] if isinstance(host_ammessi, str) else host_ammessi) if h.strip()]
        if forza_https is not None:
            self.forza_https = bool(forza_https)
        if hsts is not None:
            self.hsts = int(hsts)
        if csp is not None:
            self.csp = csp
        if compressione is not None:
            self.compressione = bool(compressione)
        if cache_statici is not None:
            self.cache_statici = int(cache_statici)
        if registro_file is not None:
            self.registro_file = registro_file
            self._log_accessi = self._crea_registro(registro_file, "accessi")
        if registro_errori is not None:
            self.registro_errori = registro_errori
            self._log_errori = self._crea_registro(registro_errori, "errori")
        if limite_globale is not None:
            self.limite_globale = tuple(limite_globale) if limite_globale else None
        if limite_accessi is not None:
            self.limite_accessi = tuple(limite_accessi)
        if timeout_connessione is not None:
            self.timeout_connessione = int(timeout_connessione)
        if connessioni_massime is not None:
            self.connessioni_massime = int(connessioni_massime)
        if self.forza_https and not self.host_ammessi:
            raise ValueError("forza_https richiede host_ammessi: senza, un visitatore potrebbe farsi reindirizzare verso un indirizzo qualsiasi")
        return self

    def _imposta_proxy(self, valore):
        self._proxy_reti, self._proxy_numero = None, 1
        if valore in (None, False, 0):
            self.proxy_fidato = False
        elif valore is True:
            self.proxy_fidato = True
        elif isinstance(valore, int):
            self.proxy_fidato, self._proxy_numero = True, valore
        else:
            self.proxy_fidato = True
            self._proxy_reti = [_indirizzi.ip_network(x, strict=False) for x in valore]

    def _crea_registro(self, percorso, nome):
        registro = _registro_py.getLogger(f"server_web.{nome}.{id(self)}")
        registro.setLevel(_registro_py.INFO)
        registro.propagate = False
        for gestore in list(registro.handlers):
            registro.removeHandler(gestore)
            gestore.close()
        cartella = _os.path.dirname(_os.path.abspath(percorso))
        _os.makedirs(cartella, exist_ok=True)
        gestore = _registro_gestori.RotatingFileHandler(percorso, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8")
        gestore.setFormatter(_registro_py.Formatter("%(message)s"))
        registro.addHandler(gestore)
        return registro

    def configura_da_ambiente(self, prefisso="SITO_", file_env=None):
        """Legge le regolazioni dalle variabili d'ambiente (e da un file .env facoltativo, le variabili vere hanno la precedenza): cosi' i segreti
        non stanno nel codice. Nomi (con il prefisso): CHIAVE_SEGRETA, PRODUZIONE, CSRF, COOKIE_SICURO, FORZA_HTTPS, HOST_AMMESSI (separati da virgole),
        PROXY_FIDATO (1, un numero, o reti separate da virgole), REGISTRO_FILE, REGISTRO_ERRORI, DIMENSIONE_MASSIMA, DURATA_SESSIONE, LIMITE_GLOBALE (es. 120/60), HSTS, CSP.
        Ritorna il dizionario di cio' che ha applicato."""
        valori = {}
        if file_env and _os.path.exists(file_env):
            with open(file_env, encoding="utf-8") as f:
                for riga in f:
                    riga = riga.strip()
                    if not riga or riga.startswith("#") or "=" not in riga:
                        continue
                    chiave, _, valore = riga.partition("=")
                    chiave = chiave.strip()
                    valore = valore.strip()
                    if len(valore) >= 2 and valore[0] == valore[-1] and valore[0] in "\"'":
                        valore = valore[1:-1]
                    valori[chiave] = valore
        for k, v in _os.environ.items():
            valori[k] = v

        def leggi(nome):
            return valori.get(prefisso + nome)

        def vero(testo):
            return str(testo).strip().lower() in ("1", "true", "si", "s\u00ec", "vero", "yes", "on")
        applicato = {}
        opzioni = {}
        if leggi("CHIAVE_SEGRETA"):
            opzioni["chiave_segreta"] = leggi("CHIAVE_SEGRETA")
        for nome, chiave in (("PRODUZIONE", "produzione"), ("CSRF", "csrf"), ("COOKIE_SICURO", "cookie_sicuro"), ("FORZA_HTTPS", "forza_https")):
            if leggi(nome) is not None:
                opzioni[chiave] = vero(leggi(nome))
        if leggi("HOST_AMMESSI"):
            opzioni["host_ammessi"] = [x for x in leggi("HOST_AMMESSI").split(",") if x.strip()]
        if leggi("PROXY_FIDATO") is not None:
            testo = leggi("PROXY_FIDATO").strip()
            if testo.isdigit():
                opzioni["proxy_fidato"] = int(testo)
            elif testo.lower() in ("0", "false", "no", ""):
                opzioni["proxy_fidato"] = False
            elif "/" in testo or "." in testo or ":" in testo:
                opzioni["proxy_fidato"] = [x.strip() for x in testo.split(",") if x.strip()]
            else:
                opzioni["proxy_fidato"] = vero(testo)
        for nome, chiave in (("REGISTRO_FILE", "registro_file"), ("REGISTRO_ERRORI", "registro_errori"), ("CSP", "csp")):
            if leggi(nome):
                opzioni[chiave] = leggi(nome)
        for nome, chiave in (("DIMENSIONE_MASSIMA", "dimensione_massima"), ("DURATA_SESSIONE", "durata_sessione"), ("HSTS", "hsts")):
            if leggi(nome):
                opzioni[chiave] = int(leggi(nome))
        if leggi("LIMITE_GLOBALE"):
            richieste, _, secondi = leggi("LIMITE_GLOBALE").partition("/")
            opzioni["limite_globale"] = (int(richieste), int(secondi or 60))
        self.configura(**opzioni)
        applicato.update({k: ("(riservato)" if k == "chiave_segreta" else v) for k, v in opzioni.items()})
        return applicato

    # ---- registrazione
    def _aggiungi(self, percorso, metodi, funzione):
        rotta = _Rotta(percorso, metodi, funzione)
        self._rotte.append(rotta)
        return rotta

    def rotta(self, percorso, metodi=("GET",)):
        """Decoratore: collega un indirizzo a una funzione."""
        if not percorso.startswith("/"):
            raise ValueError(f"l'indirizzo deve cominciare con / (invece e' {percorso!r})")

        def registra(funzione):
            self._aggiungi(percorso, metodi, funzione)
            return funzione
        return registra

    def gruppo(self, prefisso):
        """Un gruppo di rotte con un prefisso comune, gia' collegato all'applicazione."""
        return Gruppo(prefisso, self)

    def registra(self, altro, prefisso=""):
        """Collega le rotte di un Gruppo creato a parte (per esempio in un altro file)."""
        for percorso, metodi, funzione in altro._voci:
            self._aggiungi(prefisso.rstrip("/") + altro.prefisso + percorso, metodi, funzione)

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

    def dopo_ogni_richiesta(self, funzione):
        """Decoratore: `funzione(richiesta, risposta)` gira dopo ogni rotta e puo' cambiare la risposta (aggiungere intestazioni...); se ritorna qualcosa, quella e' la nuova risposta."""
        self._dopo.append(funzione)
        return funzione

    def all_avvio(self, funzione):
        """Decoratore: la funzione gira quando il server si accende (aprire il database, preparare i dati)."""
        self._all_avvio.append(funzione)
        return funzione

    def alla_chiusura(self, funzione):
        """Decoratore: la funzione gira quando il server si spegne."""
        self._alla_chiusura.append(funzione)
        return funzione

    def senza_csrf(self, funzione):
        """Decoratore (sotto @app.rotta): questa rotta non controlla il codice CSRF, per esempio un'API usata da altri programmi con un'altra autenticazione."""
        funzione._senza_csrf = True
        for r in self._rotte:
            if r.funzione is funzione:
                r.senza_csrf = True
        return funzione

    # ---- sessione, accesso
    def _firma(self, dati):
        return _b64(_hmac.new(self._chiave, dati, _hashlib.sha256).digest())

    def _leggi_sessione(self, richiesta):
        valore = richiesta.cookie.get(NOME_COOKIE_SESSIONE)
        if valore and "." in valore:
            dati, _, firma = valore.rpartition(".")
            try:
                if _hmac.compare_digest(self._firma(dati.encode()), firma):
                    contenuto = _json.loads(_unb64(dati))
                    if _tempo.time() - contenuto.get("t", 0) <= self.durata_sessione:
                        return Sessione(contenuto.get("d", {}))
            except (ValueError, TypeError):
                pass
        return Sessione()

    def _cookie_di_sessione(self, sessione):
        dati = _b64(_json.dumps({"d": dict(sessione), "t": int(_tempo.time())}, ensure_ascii=False).encode("utf-8"))
        valore = dati + "." + self._firma(dati.encode())
        if self._chiave_temporanea and not getattr(self, "_avvisato", False):
            self._avvisato = True
            print("Nota: la chiave segreta e' temporanea (le sessioni si perdono quando il server si spegne). Per tenerle: app.configura(chiave_segreta=\"un testo lungo e riservato\").", flush=True)
        if len(valore) > 3800:
            raise ErroreWeb(500, "I dati della sessione sono troppo grandi per un cookie: tieni in sessione solo poche cose (per esempio l'identificativo dell'utente)")
        return valore

    def accedi(self, richiesta, utente, **dati):
        """Segna che questo visitatore ha fatto l'accesso come `utente` (di solito il suo identificativo). Cambia il codice CSRF e scrive `dati` in sessione."""
        richiesta.sessione["utente"] = utente
        richiesta.sessione["_csrf"] = _segreti.token_urlsafe(24)
        for k, v in dati.items():
            richiesta.sessione[k] = v

    def esci(self, richiesta):
        """Toglie l'accesso e svuota la sessione."""
        richiesta.sessione.clear()

    def richiesta_corrente(self):
        """La richiesta che si sta servendo adesso (dentro una rotta o un filtro)."""
        return getattr(_locale, "richiesta", None)

    def richiede_accesso(self, funzione=None, *, login="/accedi", ruolo=None):
        """Decoratore (sotto @app.rotta): solo chi ha fatto l'accesso. Gli altri vanno alla pagina `login` (o ricevono 401 se e' un'API).
        Con ruolo="admin" serve anche che sessione["ruoli"] contenga quel ruolo (403 altrimenti)."""
        import functools

        def applica(f):
            @functools.wraps(f)
            def controllata(*a, **k):
                richiesta = self.richiesta_corrente()
                if richiesta is None or richiesta.utente is None:
                    api = richiesta is not None and (richiesta.percorso.startswith("/api") or "application/json" in (richiesta.intestazioni.get("Accept") or ""))
                    if api:
                        raise ErroreWeb(401, "Serve l'accesso")
                    destinazione = login + "?" + _url.urlencode({"prossima": richiesta.percorso if richiesta is not None else "/"})
                    return reindirizza(destinazione)
                if ruolo is not None and ruolo not in (richiesta.sessione.get("ruoli") or []):
                    raise ErroreWeb(403, "Non hai il permesso per questa pagina")
                return f(*a, **k)
            controllata._senza_csrf = getattr(f, "_senza_csrf", False)
            return controllata
        return applica(funzione) if funzione is not None else applica

    # ---- pagine
    def mostra(self, modello, richiesta=None, /, **valori):
        """Riempie un modello di pagina della cartella `cartella_pagine` e ritorna l'HTML. Con `richiesta` aggiunge ai valori: richiesta, utente,
        csrf (il codice) e campo_csrf (il campo nascosto da mettere nei moduli)."""
        contesto = dict(valori)
        richiesta = richiesta or self.richiesta_corrente()
        if richiesta is not None:
            contesto.setdefault("richiesta", richiesta)
            contesto.setdefault("utente", richiesta.utente)
            contesto.setdefault("campo_csrf", richiesta.campo_csrf)
            contesto.setdefault("csrf", richiesta.token_csrf)
        if not self.cartella_pagine:
            raise ErroreModello("manca la cartella delle pagine: app.configura(cartella_pagine=\"pagine\")")
        try:
            return _motore.carica(modello, self.cartella_pagine).rendi(contesto)
        except ErroreModello as errore:
            raise ErroreWeb(500, str(errore))

    # ---- il lavoro vero
    def _chiama(self, funzione, richiesta, argomenti):
        esito = funzione(**argomenti)
        if _ispeziona.iscoroutine(esito):
            esito = _asincrono.run(esito)
        return esito

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
        if isinstance(esito, Modello):
            return Risposta(esito.a_dizionario())
        return Risposta(esito)

    def _argomenti_semplici(self, funzione, richiesta):
        firma = _ispeziona.signature(funzione)
        return {"richiesta": richiesta} if "richiesta" in firma.parameters else {}

    def _pagina_errore(self, richiesta, stato, messaggio="", extra=None):
        funzione = self._gestori_errore.get(stato)
        if funzione:
            try:
                risposta = self._in_risposta(self._chiama(funzione, richiesta, self._argomenti_semplici(funzione, richiesta)))
                risposta.stato = stato
                return risposta
            except Exception:
                pass
        if extra is not None or richiesta.percorso.startswith("/api") or "application/json" in (richiesta.intestazioni.get("Accept") or ""):
            return Risposta({"errore": messaggio or _frase(stato), "stato": stato, **(extra or {})}, stato)
        corpo = (f"<!doctype html><meta charset=utf-8><title>{stato}</title><body style='font-family:sans-serif;margin:3em'>"
                 f"<h1>{stato} &middot; {_html.escape(_frase(stato))}</h1><p>{_html.escape(messaggio)}</p></body>")
        return Risposta(corpo, stato)

    def _cache_statici(self):
        if self.cache_statici is not None:
            return f"public, max-age={self.cache_statici}" if self.cache_statici > 0 else "no-cache"
        return "public, max-age=3600" if self.produzione else "no-cache"

    def _percorso_sicuro(self, cartella, relativo):
        """Il percorso assoluto di un file dentro `cartella`, o None se esce dalla cartella o e' un file nascosto (.env, .git...)."""
        base = _os.path.abspath(cartella)
        percorso = _os.path.abspath(_os.path.join(base, relativo))
        if percorso != base and not percorso.startswith(base + _os.sep):
            raise ErroreWeb(403, "Percorso non permesso")
        if any(pezzo.startswith(".") for pezzo in _os.path.relpath(percorso, base).replace("\\", "/").split("/") if pezzo not in (".",)):
            raise ErroreWeb(404, "File non trovato")
        return percorso

    def invia_da_cartella(self, cartella, relativo, scarica=False, nome=None):
        """Invia un file che sta dentro `cartella` (anche se `relativo` arriva dall'utente: non puo' uscire dalla cartella e i file nascosti sono rifiutati)."""
        percorso = self._percorso_sicuro(cartella, _url.unquote(relativo).lstrip("/\\"))
        if not _os.path.isfile(percorso):
            raise ErroreWeb(404, "File non trovato")
        return Risposta.da_file(percorso, scarica=scarica, nome=nome, cache=self._cache_statici())

    def _file_statico(self, richiesta):
        for prefisso, cartella in self._statici:
            if richiesta.percorso.startswith(prefisso):
                return self.invia_da_cartella(cartella, richiesta.percorso[len(prefisso):])
        return None

    def _controlla_csrf(self, richiesta, rotta):
        if not self.csrf or rotta.senza_csrf or richiesta.metodo in ("GET", "HEAD", "OPTIONS"):
            return
        atteso = richiesta.sessione.get("_csrf")
        arrivato = richiesta.form.get("csrf") or richiesta.intestazioni.get("X-CSRF-Token") or ""
        if not atteso or not _hmac.compare_digest(str(atteso), str(arrivato)):
            raise ErroreWeb(403, "Codice CSRF mancante o sbagliato: il modulo deve contenere {{ campo_csrf }} (oppure l'intestazione X-CSRF-Token)")

    def _applica_proxy(self, richiesta):
        """Con proxy_fidato: l'indirizzo vero del visitatore, lo schema (http/https) e il nome del sito vengono dalle intestazioni X-Forwarded-*."""
        richiesta.indirizzo_cliente = richiesta.cliente
        if not self.proxy_fidato:
            return
        if self._proxy_reti is not None:
            try:
                indirizzo = _indirizzi.ip_address(richiesta.cliente)
            except ValueError:
                return
            if not any(indirizzo in rete for rete in self._proxy_reti):
                return
        inoltrati = [x.strip() for x in (richiesta.intestazioni.get("X-Forwarded-For") or "").split(",") if x.strip()]
        if len(inoltrati) >= self._proxy_numero:
            richiesta.indirizzo_cliente = inoltrati[-self._proxy_numero]
        schema = (richiesta.intestazioni.get("X-Forwarded-Proto") or "").split(",")[0].strip().lower()
        if schema in ("http", "https"):
            richiesta.https = schema == "https"
        ospite = (richiesta.intestazioni.get("X-Forwarded-Host") or "").split(",")[0].strip()
        if ospite:
            richiesta._host = ospite

    def _host_ammesso(self, host):
        nome = host.strip().lower()
        if nome.startswith("["):
            nome = nome[1:nome.find("]")] if "]" in nome else nome[1:]
        elif nome.count(":") == 1:
            nome = nome.split(":")[0]
        for modello in self.host_ammessi:
            if modello == "*" or modello == nome or (modello.startswith("*.") and nome.endswith(modello[1:]) and len(nome) > len(modello) - 1):
                return True
        return False

    def _origine_ammessa(self, origine):
        if not self._cors or not origine:
            return False
        return "*" in self._cors["origini"] or origine in self._cors["origini"]

    def _controlli_iniziali(self, richiesta):
        """Prima di ogni rotta: host ammessi, HTTPS obbligatorio, limite globale, prova preliminare CORS. Ritorna una Risposta o Nessuno."""
        if richiesta.percorso in self._esenti:
            return None
        if self.host_ammessi and not self._host_ammesso(richiesta.host):
            raise ErroreWeb(400, "Host non ammesso")
        if self.forza_https and not richiesta.https:
            destinazione = "https://" + richiesta.host + richiesta.percorso + ("?" + richiesta.query_grezza if richiesta.query_grezza else "")
            return Risposta("", 308, intestazioni={"Location": destinazione})
        if self.limite_globale:
            ammesso, attesa = self._limiti.colpisci(("globale", richiesta.indirizzo_cliente), self.limite_globale[0], self.limite_globale[1])
            if not ammesso:
                raise ErroreWeb(429, "Troppe richieste: riprova fra poco", {"Retry-After": str(attesa)})
        origine = richiesta.intestazioni.get("Origin")
        if richiesta.metodo == "OPTIONS" and self._cors and origine and richiesta.intestazioni.get("Access-Control-Request-Method"):
            if self._origine_ammessa(origine):
                return Risposta("", 204, intestazioni={"Access-Control-Max-Age": str(self._cors["durata"])})
        return None

    def _errore_interno(self, richiesta, errore):
        import traceback
        testo = traceback.format_exc()
        _sistema.stderr.write(f"[{richiesta.id}] {richiesta.metodo} {richiesta.percorso}\n{testo}")
        if self._log_errori is not None:
            self._log_errori.error(f"{_tempo.strftime('%Y-%m-%dT%H:%M:%S%z')} id={richiesta.id} {richiesta.indirizzo_cliente} {richiesta.metodo} {richiesta.percorso}\n{testo}")
        if self.produzione:
            return self._pagina_errore(richiesta, 500, f"Errore interno del server. Codice: {richiesta.id}", {"codice": richiesta.id})
        return self._pagina_errore(richiesta, 500, "Errore nel programma: " + type(errore).__name__ + ": " + str(errore))

    def _smista(self, richiesta):
        try:
            iniziale = self._controlli_iniziali(richiesta)
            if iniziale is not None:
                return iniziale
            for prima in self._prima:
                esito = self._chiama(prima, richiesta, self._argomenti_semplici(prima, richiesta))
                if esito is not None:
                    return self._in_risposta(esito)
            metodi_permessi = set()
            for rotta in self._rotte:
                valori = rotta.corrisponde(richiesta.percorso)
                if valori is None:
                    continue
                metodo = "GET" if richiesta.metodo == "HEAD" else richiesta.metodo
                if metodo in rotta.metodi:
                    self._controlla_csrf(richiesta, rotta)
                    return self._in_risposta(self._chiama(rotta.funzione, richiesta, rotta.associa(richiesta, valori)))
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
        except ErroreValidazione as errore:
            return self._pagina_errore(richiesta, 422, "Dati non validi", {"errori": errore.errori})
        except ErroreWeb as errore:
            risposta = self._pagina_errore(richiesta, errore.stato, errore.messaggio)
            risposta.intestazioni.update(errore.intestazioni)
            return risposta
        except Exception as errore:
            return self._errore_interno(richiesta, errore)

    def _non_modificata(self, risposta):
        nuova = Risposta("", 304)
        for k in ("ETag", "Last-Modified", "Cache-Control", "Vary"):
            if k in risposta.intestazioni:
                nuova.intestazioni[k] = risposta.intestazioni[k]
        nuova.cookie = list(risposta.cookie)
        return nuova

    def _condizionale(self, richiesta, risposta):
        """If-None-Match / If-Modified-Since: se il browser ha gia' la versione giusta risponde 304 senza ripetere il file."""
        if richiesta.metodo not in ("GET", "HEAD") or risposta.stato != 200:
            return risposta
        etag, ultima = risposta.intestazioni.get("ETag"), risposta.intestazioni.get("Last-Modified")
        if not etag and not ultima:
            return risposta
        senza_debole = lambda t: t[2:] if t.startswith("W/") else t
        arrivati = richiesta.intestazioni.get("If-None-Match")
        if arrivati:
            elenco = [t.strip() for t in arrivati.split(",")]
            if etag and ("*" in elenco or any(senza_debole(t) == senza_debole(etag) for t in elenco)):
                return self._non_modificata(risposta)
            return risposta
        posseduta = richiesta.intestazioni.get("If-Modified-Since")
        if ultima and posseduta:
            try:
                if _email_utili.parsedate_to_datetime(ultima).timestamp() <= _email_utili.parsedate_to_datetime(posseduta).timestamp():
                    return self._non_modificata(risposta)
            except (TypeError, ValueError):
                pass
        return risposta

    def _intervallo(self, richiesta, risposta):
        """Range: «dammi i byte da a a b» (serve a video, audio, PDF e ai download ripresi)."""
        if not risposta.in_flusso or richiesta.metodo != "GET" or risposta.stato != 200:
            return risposta
        richiesto = richiesta.intestazioni.get("Range")
        if not richiesto:
            return risposta
        m = _re.fullmatch(r"bytes=(\d*)-(\d*)", richiesto.strip())
        if not m or (not m.group(1) and not m.group(2)):
            return risposta
        totale = risposta._dimensione_file
        if m.group(1) == "":
            inizio, fine = max(0, totale - int(m.group(2))), totale - 1
        else:
            inizio, fine = int(m.group(1)), min(int(m.group(2)) if m.group(2) else totale - 1, totale - 1)
        if inizio > fine or inizio >= totale:
            return Risposta("", 416, intestazioni={"Content-Range": f"bytes */{totale}"})
        risposta._intervallo = (inizio, fine)
        risposta.stato = 206
        risposta.intestazioni["Content-Range"] = f"bytes {inizio}-{fine}/{totale}"
        return risposta

    def _comprimi(self, richiesta, risposta):
        if (not self.compressione or risposta.in_flusso or risposta.stato in (204, 304, 206) or "Content-Encoding" in risposta.intestazioni
                or "gzip" not in (richiesta.intestazioni.get("Accept-Encoding") or "").lower()):
            return
        tipo = risposta.tipo.split(";")[0].strip().lower()
        if not (tipo.startswith("text/") or tipo in ("application/json", "application/javascript", "application/xml", "image/svg+xml")):
            return
        dati = risposta._corpo
        if len(dati) < 600 or len(dati) > 5 * 1024 * 1024:
            return
        compresso = _gzip.compress(dati, 5, mtime=0)
        if len(compresso) >= len(dati):
            return
        risposta._corpo = compresso
        risposta.intestazioni["Content-Encoding"] = "gzip"
        risposta.intestazioni["Vary"] = (risposta.intestazioni["Vary"] + ", Accept-Encoding") if risposta.intestazioni.get("Vary") else "Accept-Encoding"

    def _finisci(self, richiesta, risposta):
        """Dopo la rotta: filtri, cookie di sessione, intestazioni di sicurezza, CORS, cache, intervalli e compressione."""
        for dopo in self._dopo:
            try:
                argomenti = {}
                nomi = _ispeziona.signature(dopo).parameters
                if "richiesta" in nomi:
                    argomenti["richiesta"] = richiesta
                if "risposta" in nomi:
                    argomenti["risposta"] = risposta
                nuova = dopo(**argomenti) if argomenti else dopo(richiesta, risposta)
                if nuova is not None:
                    risposta = self._in_risposta(nuova)
            except ErroreWeb as errore:
                risposta = self._pagina_errore(richiesta, errore.stato, errore.messaggio)
            except Exception as errore:
                risposta = self._errore_interno(richiesta, errore)
        sessione = richiesta._sessione
        if sessione is not None and sessione.modificata:
            sicuro = self.cookie_sicuro or richiesta.https or self._https
            if len(sessione) == 0:
                risposta.togli_cookie(NOME_COOKIE_SESSIONE)
            else:
                try:
                    risposta.imposta_cookie(NOME_COOKIE_SESSIONE, self._cookie_di_sessione(sessione), durata=self.durata_sessione, sicuro=sicuro)
                except ErroreWeb as errore:
                    risposta = self._pagina_errore(richiesta, errore.stato, errore.messaggio)
        for k, v in self.intestazioni_sicurezza.items():
            risposta.intestazioni.setdefault(k, v)
        if self.csp:
            risposta.intestazioni.setdefault("Content-Security-Policy", self.csp)
        if (richiesta.https or self._https) and (self.hsts or (self.hsts is None and self.produzione)):
            risposta.intestazioni.setdefault("Strict-Transport-Security", f"max-age={self.hsts or 31536000}; includeSubDomains")
        origine = richiesta.intestazioni.get("Origin")
        if self._origine_ammessa(origine):
            c = self._cors
            risposta.intestazioni["Access-Control-Allow-Origin"] = "*" if ("*" in c["origini"] and not c["credenziali"]) else origine
            risposta.intestazioni["Vary"] = (risposta.intestazioni["Vary"] + ", Origin") if risposta.intestazioni.get("Vary") else "Origin"
            if c["credenziali"]:
                risposta.intestazioni["Access-Control-Allow-Credentials"] = "true"
            if richiesta.metodo == "OPTIONS" and richiesta.intestazioni.get("Access-Control-Request-Method"):
                risposta.intestazioni["Access-Control-Allow-Methods"] = ", ".join(c["metodi"])
                risposta.intestazioni["Access-Control-Allow-Headers"] = ", ".join(c["intestazioni"])
        risposta.intestazioni["X-Request-ID"] = richiesta.id
        if not risposta.in_flusso:
            risposta.intestazioni.setdefault("Cache-Control", "no-store")
        risposta = self._condizionale(richiesta, risposta)
        risposta = self._intervallo(richiesta, risposta)
        self._comprimi(richiesta, risposta)
        return risposta

    def _registra_accesso(self, richiesta, risposta):
        ms = int((_tempo.time() - richiesta.inizio) * 1000)
        if self._log_accessi is not None:
            self._log_accessi.info(f"{_tempo.strftime('%Y-%m-%dT%H:%M:%S%z')} {richiesta.indirizzo_cliente} {richiesta.metodo} {richiesta.percorso} {risposta.stato} {ms}ms id={richiesta.id}")
        if self.registro and richiesta.cliente != "simulato":
            print(f"{richiesta.metodo} {richiesta.percorso} {risposta.stato} ({ms} ms)", flush=True)

    def risposta_a(self, richiesta):
        """Trova la rotta giusta per una richiesta e ne ricava la risposta (non scrive nulla sulla rete: si puo' provare anche da soli)."""
        richiesta._app = self
        self._applica_proxy(richiesta)
        _locale.richiesta = richiesta
        try:
            risposta = self._smista(richiesta)
        finally:
            _locale.richiesta = None
        risposta = self._finisci(richiesta, risposta)
        self._registra_accesso(richiesta, risposta)
        return risposta

    def _risposta_diretta(self, richiesta, stato, messaggio):
        """Per gli errori che si decidono prima di leggere la richiesta (corpo troppo grande, trasferimento a pezzi...)."""
        richiesta._app = self
        self._applica_proxy(richiesta)
        risposta = self._finisci(richiesta, self._pagina_errore(richiesta, stato, messaggio))
        self._registra_accesso(richiesta, risposta)
        return risposta

    def _uscita(self, richiesta, risposta):
        """Le intestazioni da inviare e se c'e' un corpo: ([(nome, valore)], invia_corpo)."""
        senza_corpo = risposta.stato in (204, 304) or 100 <= risposta.stato < 200
        intestazioni = []
        if not senza_corpo:
            intestazioni += [("Content-Type", risposta.tipo), ("Content-Length", str(risposta.lunghezza))]
        intestazioni += [(k, v) for k, v in risposta.intestazioni.items() if k.lower() not in ("content-length", "content-type")]
        intestazioni += [("Set-Cookie", c) for c in risposta.cookie]
        return intestazioni, (not senza_corpo and richiesta.metodo != "HEAD")

    # ---- limiti di richieste e blocco degli accessi
    def limita(self, richieste, secondi=60, per="ip"):
        """Decoratore (sotto @app.rotta): al massimo `richieste` ogni `secondi` secondi per ogni indirizzo IP (per="utente": per ogni utente che ha fatto l'accesso).
        Oltre il limite la risposta e' 429 con Retry-After. Serve soprattutto sulle pagine di accesso e di registrazione.
        I contatori stanno nella memoria del programma: con piu' processi ognuno ha i suoi."""
        import functools

        def applica(f):
            @functools.wraps(f)
            def limitata(*a, **k):
                richiesta = self.richiesta_corrente()
                if richiesta is not None:
                    soggetto = richiesta.utente if (per == "utente" and richiesta.utente is not None) else richiesta.indirizzo_cliente
                    ammesso, attesa = self._limiti.colpisci((f.__module__, f.__qualname__, soggetto), richieste, secondi)
                    if not ammesso:
                        raise ErroreWeb(429, "Troppe richieste: riprova fra poco", {"Retry-After": str(attesa)})
                return f(*a, **k)
            limitata._senza_csrf = getattr(f, "_senza_csrf", False)
            limitata._limitata = True
            return limitata
        return applica

    def accesso_bloccato(self, chiave):
        """I secondi che mancano alla fine del blocco di questa chiave (di solito nome utente + indirizzo), o 0 se non e' bloccata."""
        with self._blocco_tentativi:
            voce = self._tentativi.get(chiave)
            if voce and voce["bloccato_fino"] > _tempo.time():
                return int(voce["bloccato_fino"] - _tempo.time()) + 1
        return 0

    def accesso_fallito(self, chiave):
        """Registra un tentativo di accesso sbagliato. Dopo `tentativi` errori entro `finestra` secondi la chiave resta bloccata per `blocco` secondi
        (app.configura(limite_accessi=(tentativi, finestra, blocco))). Ritorna i secondi di blocco (0 se non e' ancora bloccata)."""
        massimo, finestra, blocco = self.limite_accessi
        ora = _tempo.time()
        with self._blocco_tentativi:
            if len(self._tentativi) > 20000:
                self._tentativi = {k: v for k, v in self._tentativi.items() if v["bloccato_fino"] > ora or ora - v["inizio"] < finestra}
            voce = self._tentativi.get(chiave)
            if voce is None or (ora - voce["inizio"] > finestra and voce["bloccato_fino"] <= ora):
                voce = {"conteggio": 0, "inizio": ora, "bloccato_fino": 0}
                self._tentativi[chiave] = voce
            voce["conteggio"] += 1
            if voce["conteggio"] >= massimo:
                voce["bloccato_fino"] = ora + blocco
                voce["conteggio"] = 0
                voce["inizio"] = ora
                return blocco
        return 0

    def accesso_riuscito(self, chiave):
        """Azzera i tentativi sbagliati di questa chiave."""
        with self._blocco_tentativi:
            self._tentativi.pop(chiave, None)

    def cors(self, origini, metodi=("GET", "POST", "PUT", "PATCH", "DELETE"), intestazioni=("Content-Type", "Authorization", "X-CSRF-Token"), credenziali=False, durata=600):
        """Permette a pagine di altri siti (le `origini`, per esempio ["https://app.esempio.it"]) di chiamare questa API dal browser. "*" = tutti (senza cookie)."""
        if credenziali and "*" in origini:
            raise ValueError("con credenziali=Vero bisogna elencare le origini: \"*\" non e' permesso")
        self._cors = {"origini": list(origini), "metodi": list(metodi), "intestazioni": list(intestazioni), "credenziali": bool(credenziali), "durata": int(durata)}

    def salute(self, percorso="/salute", controlla=None):
        """Una pagina per controllare che il sito sia vivo (per Docker, i bilanciatori, i servizi di monitoraggio): {"stato": "ok"}. `controlla` e' una funzione facoltativa
        (per esempio apre il database): se solleva un errore la risposta e' 503. Non e' soggetta a host, HTTPS e limiti."""
        app = self

        def stato_salute():
            if controlla is not None:
                try:
                    controlla()
                except Exception as errore:
                    raise ErroreWeb(503, "Non pronto: " + type(errore).__name__)
            return {"stato": "ok", "applicazione": app.nome, "secondi": int(_tempo.time() - app._avvio_tempo)}
        rotta = self._aggiungi(percorso, ("GET", "HEAD"), stato_salute)
        rotta.nascosta = True
        self._esenti.add(percorso)

    # ---- controllo prima di pubblicare
    def controlla_produzione(self, ascolta=None):
        """Cosa manca per pubblicare il sito: un elenco di {gravita, problema, correzione}. gravita: "errore" (non pubblicare cosi'), "attenzione", "nota"."""
        problemi = []

        def segna(gravita, problema, correzione):
            problemi.append({"gravita": gravita, "problema": problema, "correzione": correzione})
        ascolta = ascolta if ascolta is not None else self._ascolta
        if not self.produzione:
            segna("errore", "Il sito non e' in modalita' produzione: un errore mostrerebbe ai visitatori i dettagli interni.", "app.configura(produzione=Vero)")
        if self._chiave_temporanea:
            segna("errore", "La chiave segreta e' temporanea: le sessioni si perdono a ogni riavvio e non reggono con piu' processi.",
                  "app.configura(chiave_segreta=...) con un testo lungo e riservato (meglio da una variabile d'ambiente: app.configura_da_ambiente())")
        if not self.host_ammessi:
            segna("errore", "Mancano gli host ammessi: il sito risponderebbe a qualsiasi nome (usato per falsificare link e reindirizzamenti).", "app.configura(host_ammessi=[\"esempio.it\"])")
        scrivono = [r for r in self._rotte if not r.nascosta and any(m not in ("GET", "HEAD", "OPTIONS") for m in r.metodi) and not r.senza_csrf]
        if scrivono and not self.csrf:
            segna("attenzione", "Ci sono rotte che modificano dati (POST/PUT/DELETE) ma la protezione CSRF e' spenta.", "app.configura(csrf=Vero) (e {{ campo_csrf }} nei moduli)")
        if not (self.cookie_sicuro or self.proxy_fidato or self._https):
            segna("attenzione", "I cookie di sessione non sono marcati «Secure» e il sito non sa di essere in HTTPS.",
                  "metti un proxy HTTPS davanti con app.configura(proxy_fidato=Vero), oppure cookie_sicuro=Vero")
        if ascolta in ("0.0.0.0", "::") and not self.proxy_fidato:
            segna("attenzione", "Il sito ascolta su tutte le interfacce senza un proxy davanti: niente HTTPS e IP dei visitatori non affidabili.", "usa ascolta=\"127.0.0.1\" dietro un proxy (Caddy, nginx) con proxy_fidato=Vero")
        if self.proxy_fidato and self._proxy_reti is None and ascolta in ("0.0.0.0", "::"):
            segna("attenzione", "proxy_fidato=Vero con il sito raggiungibile da tutti: chi si collega direttamente puo' falsificare X-Forwarded-For.",
                  "non pubblicare la porta del sito (solo il proxy la raggiunge) o elenca le reti del proxy: proxy_fidato=[\"172.16.0.0/12\"]")
        sensibili = [r for r in self._rotte if any(p in r.modello.lower() for p in ("accedi", "login", "password", "registra", "iscriviti", "reimposta")) and any(m == "POST" for m in r.metodi)]
        senza_limite = [r for r in sensibili if not getattr(r.funzione, "_limitata", False)]
        if senza_limite and not self.limite_globale:
            segna("attenzione", "Le pagine di accesso/registrazione (" + ", ".join(sorted({r.modello for r in senza_limite})) + ") non hanno un limite di tentativi.",
                  "@app.limita(5, 60) sulla rotta, e app.accesso_fallito(chiave) / app.accesso_bloccato(chiave) per bloccare chi indovina le password")
        if self._documentazione:
            segna("nota", "La documentazione automatica e' attiva: in produzione e' spenta a meno che non la accendi (attiva_in_produzione=Vero).", "tienila spenta se l'API non e' pubblica")
        if not self.registro_file:
            segna("nota", "Non c'e' un registro degli accessi su file.", "app.configura(registro_file=\"logs/accessi.log\", registro_errori=\"logs/errori.log\")")
        if (self._https or self.proxy_fidato) and self.hsts is None and not self.produzione:
            segna("nota", "HSTS (obbliga il browser a usare sempre HTTPS) parte da solo solo in produzione.", "app.configura(hsts=31536000)")
        return problemi

    def stampa_controllo_produzione(self, problemi=None, ascolta=None):
        """Scrive il risultato di controlla_produzione in modo leggibile."""
        problemi = problemi if problemi is not None else self.controlla_produzione(ascolta)
        if not problemi:
            print("Controllo per la produzione: tutto a posto.", flush=True)
        for p in problemi:
            etichetta = {"errore": "ERRORE", "attenzione": "ATTENZIONE", "nota": "nota"}[p["gravita"]]
            print(f"  [{etichetta}] {p['problema']}\n      -> {p['correzione']}", flush=True)
        return problemi

    # ---- provare senza rete
    def simula(self, percorso, metodo="GET", json=None, form=None, intestazioni=None, cookie=None, file=None, indirizzo=None, https=False, host=None):
        """Prova una rotta senza accendere il server e senza rete: ritorna la Risposta (stato, testo, dati, intestazioni).

            r = app.simula("/saluta/Ada")           r.stato -> 200,  r.dati -> {"messaggio": "Ciao Ada"}
            r = app.simula("/voci", "POST", json={"titolo": "pane"})
            r = app.simula("/modulo", "POST", form={"nome": "Ada"})
        Serve per imparare e per i test automatici del tuo sito. Per provare un percorso intero (accesso, sessione, cookie) usa app.cliente().
        indirizzo="1.2.3.4" finge un altro visitatore (per i limiti di richieste), https=Vero e host="esempio.it" fingono la connessione."""
        parti = _url.urlsplit(percorso)
        intestazioni = dict(intestazioni or {})
        corpo = b""
        if json is not None:
            corpo = _json.dumps(json).encode("utf-8")
            intestazioni["Content-Type"] = "application/json"
        elif file is not None:
            confine = "----prova" + _segreti.token_hex(8)
            pezzi = []
            for k, v in (form or {}).items():
                pezzi.append(f'--{confine}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode("utf-8"))
            for k, (nome_file, dati) in file.items():
                dati = dati.encode("utf-8") if isinstance(dati, str) else dati
                pezzi.append(f'--{confine}\r\nContent-Disposition: form-data; name="{k}"; filename="{nome_file}"\r\nContent-Type: application/octet-stream\r\n\r\n'.encode("utf-8")
                             + dati + b"\r\n")
            corpo = b"".join(pezzi) + f"--{confine}--\r\n".encode()
            intestazioni["Content-Type"] = f"multipart/form-data; boundary={confine}"
        elif form is not None:
            corpo = _url.urlencode(form).encode("utf-8")
            intestazioni["Content-Type"] = "application/x-www-form-urlencoded"
        if cookie:
            intestazioni["Cookie"] = "; ".join(f"{k}={v}" for k, v in cookie.items())
        if host:
            intestazioni["Host"] = host
        richiesta = Richiesta(metodo.upper(), _url.unquote(parti.path), _url.parse_qs(parti.query, keep_blank_values=True), intestazioni, corpo, indirizzo or "simulato")
        richiesta.https = bool(https)
        return self.risposta_a(richiesta)

    def cliente(self):
        """Un «browser» finto che ricorda i cookie tra una richiesta e l'altra: serve a provare accessi, sessioni e moduli con CSRF."""
        return ClienteProva(self)

    # ---- documentazione automatica
    def openapi(self, titolo=None, versione="1.0"):
        """La descrizione del sito nel formato OpenAPI 3 (un dizionario): indirizzi, parametri, corpi JSON e risposte."""
        percorsi = {}
        for rotta in self._rotte:
            if rotta.nascosta:
                continue
            modello = _re.sub(r"<(?:(\w+):)?(\w+)>", lambda m: "{" + (m.group(2) if m.group(2) not in _TIPI_PARAMETRO or m.group(1) in _TIPI_PARAMETRO else m.group(1)) + "}", rotta.modello)
            voce = percorsi.setdefault(modello, {})
            doc = _ispeziona.getdoc(rotta.funzione) or ""
            for metodo in rotta.metodi:
                operazione = {"operationId": f"{rotta.funzione.__name__}_{metodo.lower()}", "summary": doc.split("\n")[0] if doc else rotta.funzione.__name__,
                              "parameters": [], "responses": {"200": {"description": "Risposta riuscita"}}}
                if "\n" in doc.strip():
                    operazione["description"] = doc.strip()
                convalidato = False
                for nome, dove, tipo, predefinito in rotta.parametri_della_funzione():
                    if dove == "richiesta":
                        continue
                    if dove == "corpo":
                        operazione["requestBody"] = {"required": predefinito is _OBBLIGATORIO,
                                                     "content": {"application/json": {"schema": _schema(tipo) if tipo is not _ispeziona.Parameter.empty else {"type": "object"}}}}
                        convalidato = True
                        continue
                    parametro = {"name": nome, "in": "path" if dove == "indirizzo" else "query", "required": dove == "indirizzo" or predefinito is _OBBLIGATORIO,
                                 "schema": _schema(tipo if tipo is not _ispeziona.Parameter.empty else (int if nome in rotta.tipi else str))}
                    if predefinito is not _OBBLIGATORIO and dove == "query" and isinstance(predefinito, (str, int, float, bool)):
                        parametro["schema"]["default"] = predefinito
                    operazione["parameters"].append(parametro)
                    convalidato = True
                if convalidato:
                    operazione["responses"]["422"] = {"description": "Dati non validi"}
                voce[metodo.lower()] = operazione
        return {"openapi": "3.0.3", "info": {"title": titolo or self.nome, "version": versione}, "paths": percorsi}

    def documentazione(self, percorso="/docs", titolo=None, versione="1.0", attiva_in_produzione=False):
        """Attiva la documentazione automatica: `percorso` (pagina leggibile) e `/openapi.json` (da aprire con Swagger, Postman...).
        In produzione resta spenta (risponde 404) a meno che non scrivi attiva_in_produzione=Vero: l'elenco delle rotte aiuta chi attacca."""
        app = self

        def visibile():
            if app.produzione and not attiva_in_produzione:
                raise ErroreWeb(404, "Pagina non trovata")

        def pagina_docs():
            visibile()
            return _pagina_documentazione(app.openapi(titolo, versione), percorso)

        def schema_json():
            visibile()
            return app.openapi(titolo, versione)
        self._rotte = [r for r in self._rotte if not getattr(r, "e_documentazione", False)]        # richiamarla di nuovo sostituisce la precedente
        r1 = self._aggiungi(percorso, ("GET",), pagina_docs)
        r2 = self._aggiungi("/openapi.json", ("GET",), schema_json)
        r1.nascosta = r2.nascosta = r1.e_documentazione = r2.e_documentazione = True
        self._documentazione = percorso

    # ---- server
    def _crea_server(self, porta, ascolta, certificato=None, chiave=None):
        app = self

        class Gestore(_Gestore):
            protocol_version = "HTTP/1.1"
            server_version = "server_web"
            sys_version = ""

            def version_string(self):
                return "server_web"
            timeout = app.timeout_connessione

            def setup(self):
                _Gestore.setup(self)
                self._conta = 0

            def _servi(self):
                self._conta += 1
                url = _url.urlsplit(self.path)
                limite = app.dimensione_massima if app.dimensione_massima is not None else DIMENSIONE_MASSIMA
                try:
                    lunghezza = int(self.headers.get("Content-Length") or 0)
                except ValueError:
                    lunghezza = 0
                vuota = Richiesta(self.command, _url.unquote(url.path), _url.parse_qs(url.query, keep_blank_values=True), self.headers, b"", self.client_address[0])
                vuota.https = app._https
                if "chunked" in (self.headers.get("Transfer-Encoding") or "").lower():
                    richiesta, risposta = vuota, app._risposta_diretta(vuota, 411, "Il trasferimento a pezzi non e' supportato: serve Content-Length")
                    self.close_connection = True
                elif lunghezza < 0 or lunghezza > limite:
                    richiesta, risposta = vuota, app._risposta_diretta(vuota, 413, "Richiesta troppo grande")
                    self.close_connection = True
                else:
                    try:
                        corpo = self.rfile.read(lunghezza) if lunghezza > 0 else b""
                    except (TimeoutError, OSError):
                        self.close_connection = True
                        return
                    richiesta = Richiesta(self.command, _url.unquote(url.path), _url.parse_qs(url.query, keep_blank_values=True), self.headers, corpo,
                                          self.client_address[0])
                    richiesta.https = app._https
                    risposta = app.risposta_a(richiesta)
                intestazioni, invia_corpo = app._uscita(richiesta, risposta)
                self.send_response(risposta.stato)
                for k, v in intestazioni:
                    self.send_header(k, v)
                if self._conta >= MAX_RICHIESTE_PER_CONNESSIONE:
                    self.send_header("Connection", "close")
                    self.close_connection = True
                self.end_headers()
                if invia_corpo:
                    for pezzo in risposta.blocchi():
                        self.wfile.write(pezzo)

            do_GET = do_POST = do_PUT = do_PATCH = do_DELETE = do_HEAD = do_OPTIONS = _servi

            def log_message(self, formato, *argomenti):        # il registro lo scriviamo noi, in italiano
                pass

        _Server.allow_reuse_address = True
        server = _ServerRobusto((ascolta, porta), Gestore, self.connessioni_massime)
        server.daemon_threads = True
        if certificato:
            contesto = _ssl.SSLContext(_ssl.PROTOCOL_TLS_SERVER)
            contesto.minimum_version = _ssl.TLSVersion.TLSv1_2
            contesto.load_cert_chain(certificato, chiave)
            server.socket = contesto.wrap_socket(server.socket, server_side=True)
            self._https = True
        return server

    def _installa_sigterm(self):
        """Lo spegnimento da parte del sistema (docker stop, systemctl stop) diventa un arresto pulito, come Ctrl+C."""
        if _thread.current_thread() is not _thread.main_thread():
            return

        def termina(numero, quadro):
            raise KeyboardInterrupt()
        try:
            _segnali.signal(_segnali.SIGTERM, termina)
        except (ValueError, OSError, AttributeError):
            pass

    def avvia(self, porta=8000, ascolta="127.0.0.1", apri_browser=False, certificato=None, chiave=None):
        """Accende il server integrato e resta qui finche' non lo spegni (Ctrl+C, SIGTERM, oppure «Ferma» in PitStudio). Scrive l'indirizzo, cosi' si puo' cliccare.
        E' pensato per imparare e per strumenti locali: per un sito pubblico usa avvia_produzione().
        Con certificato="cert.pem" e chiave="chiave.pem" il sito e' in HTTPS (https://...): serve un certificato (per provare: mkcert o openssl)."""
        self._ascolta = ascolta
        server = self._crea_server(porta, ascolta, certificato, chiave)
        schema = "https" if certificato else "http"
        indirizzo = f"{schema}://{'127.0.0.1' if ascolta in ('0.0.0.0', '') else ascolta}:{server.server_address[1]}/"
        print(f"Server in ascolto su {indirizzo}  (per spegnerlo: Ctrl+C o Ferma)", flush=True)
        if ascolta in ("0.0.0.0", ""):
            print("Attenzione: lo vedono tutti i computer della rete.", flush=True)
        if self._documentazione:
            print(f"Documentazione: {indirizzo.rstrip('/')}{self._documentazione}", flush=True)
        for funzione in self._all_avvio:
            funzione()
        if apri_browser:
            _thread.Timer(0.4, lambda: _browser.open(indirizzo)).start()
        self._installa_sigterm()
        try:
            server.serve_forever(poll_interval=0.2)
        except KeyboardInterrupt:
            print("Server spento.", flush=True)
        finally:
            server.server_close()
            for funzione in self._alla_chiusura:
                funzione()

    def avvia_in_sottofondo(self, porta=0, ascolta="127.0.0.1", certificato=None, chiave=None):
        """Accende il server senza bloccare il programma (utile con una finestra tkinter, o per le prove). porta=0 sceglie una porta libera.
        Ritorna un oggetto con .indirizzo, .porta e .ferma()."""
        server = self._crea_server(porta, ascolta, certificato, chiave)
        for funzione in self._all_avvio:
            funzione()
        filo = _thread.Thread(target=lambda: server.serve_forever(poll_interval=0.1), daemon=True)
        filo.start()
        return ServerAvviato(server, filo, "https" if certificato else "http", self)

    # ---- il server di produzione (waitress)
    def _crea_server_produzione(self, porta, ascolta, filo=8, **opzioni):
        try:
            from waitress.server import create_server
        except ImportError:
            raise ErroreProduzione("Per pubblicare serve waitress, il server di produzione: e' incluso in PitStudio; se manca installalo con `pip install waitress` "
                                   "(in PitStudio: pannello Pacchetti).")
        limite = self.dimensione_massima if self.dimensione_massima is not None else DIMENSIONE_MASSIMA
        parametri = dict(host=ascolta, port=porta, threads=filo, ident="server_web", channel_timeout=self.timeout_connessione,
                         max_request_body_size=limite, connection_limit=self.connessioni_massime,
                         clear_untrusted_proxy_headers=False)          # le intestazioni X-Forwarded-* le legge server_web stessa (proxy_fidato)
        parametri.update(opzioni)
        return create_server(self, **parametri)

    def avvia_produzione(self, porta=8000, ascolta="127.0.0.1", filo=8, ignora_controlli=False, **opzioni_waitress):
        """Accende il sito con waitress, un server di produzione (Windows, Linux, macOS), dietro un proxy HTTPS (Caddy, nginx...).
        Prima fa il controllo di controlla_produzione(): se c'e' un ERRORE non parte (ignora_controlli=Vero per partire lo stesso, a tuo rischio).
        Si ferma con Ctrl+C o con SIGTERM (docker stop, systemctl stop): chiude le richieste in corso e poi esce."""
        self._ascolta = ascolta
        problemi = self.controlla_produzione(ascolta)
        self.stampa_controllo_produzione(problemi)
        if not ignora_controlli and any(p["gravita"] == "errore" for p in problemi):
            raise ErroreProduzione("Il sito non e' pronto per la produzione (vedi gli ERRORE qui sopra). Correggili, oppure avvia_produzione(ignora_controlli=Vero).")
        server = self._crea_server_produzione(porta, ascolta, filo, **opzioni_waitress)
        print(f"Sito in produzione su http://{ascolta}:{server.effective_port}/  (waitress, {filo} fili; per spegnerlo: Ctrl+C o SIGTERM)", flush=True)
        for funzione in self._all_avvio:
            funzione()
        self._installa_sigterm()
        try:
            server.run()
        except KeyboardInterrupt:
            pass
        finally:
            server.close()
            print("Server spento.", flush=True)
            for funzione in self._alla_chiusura:
                funzione()

    def avvia_produzione_in_sottofondo(self, porta=0, ascolta="127.0.0.1", filo=4, **opzioni_waitress):
        """Come avvia_produzione ma senza bloccare e senza controlli (per le prove). Ritorna un oggetto con .indirizzo, .porta e .ferma()."""
        server = self._crea_server_produzione(porta, ascolta, filo, **opzioni_waitress)
        for funzione in self._all_avvio:
            funzione()
        esecuzione = _thread.Thread(target=server.run, daemon=True)
        esecuzione.start()
        return _ServerProduzione(server, esecuzione, self)

    # ---- WSGI e ASGI: per i server di produzione
    def __call__(self, ambiente, avvia_risposta):
        """Interfaccia WSGI: l'applicazione stessa si puo' dare a waitress, gunicorn, mod_wsgi...  (es.: waitress.serve(app, port=8000))."""
        try:
            lunghezza = int(ambiente.get("CONTENT_LENGTH") or 0)
        except ValueError:
            lunghezza = 0
        limite = self.dimensione_massima if self.dimensione_massima is not None else DIMENSIONE_MASSIMA
        intestazioni = {}
        for k, v in ambiente.items():
            if k.startswith("HTTP_"):
                intestazioni[k[5:].replace("_", "-").title()] = v
        if ambiente.get("CONTENT_TYPE"):
            intestazioni["Content-Type"] = ambiente["CONTENT_TYPE"]
        percorso = (ambiente.get("PATH_INFO") or "/").encode("latin-1", "replace").decode("utf-8", "replace")
        query = _url.parse_qs(ambiente.get("QUERY_STRING") or "", keep_blank_values=True)
        metodo = ambiente.get("REQUEST_METHOD", "GET")
        cliente = ambiente.get("REMOTE_ADDR", "")
        if lunghezza < 0 or lunghezza > limite:
            richiesta = Richiesta(metodo, percorso, query, intestazioni, b"", cliente)
            richiesta.https = ambiente.get("wsgi.url_scheme") == "https"
            risposta = self._risposta_diretta(richiesta, 413, "Richiesta troppo grande")
        else:
            corpo = ambiente["wsgi.input"].read(lunghezza) if lunghezza > 0 else b""
            richiesta = Richiesta(metodo, percorso, query, intestazioni, corpo, cliente)
            richiesta.https = ambiente.get("wsgi.url_scheme") == "https"
            risposta = self.risposta_a(richiesta)
        uscita, invia_corpo = self._uscita(richiesta, risposta)
        avvia_risposta(f"{risposta.stato} {_frase(risposta.stato)}", uscita)
        return risposta.blocchi() if invia_corpo else iter(())

    @property
    def asgi(self):
        """Interfaccia ASGI: `uvicorn.run(app.asgi)` o `hypercorn`. Le rotte girano in un filo a parte, quindi non bloccano il server."""
        app = self

        async def applicazione(ambito, ricevi, invia):
            if ambito["type"] == "lifespan":
                while True:
                    messaggio = await ricevi()
                    if messaggio["type"] == "lifespan.startup":
                        for funzione in app._all_avvio:
                            funzione()
                        await invia({"type": "lifespan.startup.complete"})
                    elif messaggio["type"] == "lifespan.shutdown":
                        for funzione in app._alla_chiusura:
                            funzione()
                        await invia({"type": "lifespan.shutdown.complete"})
                        return
            if ambito["type"] != "http":
                return
            corpo = b""
            limite = app.dimensione_massima if app.dimensione_massima is not None else DIMENSIONE_MASSIMA
            troppo_grande = False
            while True:
                messaggio = await ricevi()
                corpo += messaggio.get("body", b"")
                if len(corpo) > limite:
                    troppo_grande = True
                    corpo = b""
                if not messaggio.get("more_body"):
                    break
            intestazioni = {}
            for k, v in ambito.get("headers", []):
                nome = k.decode("latin-1").title()
                valore = v.decode("latin-1")
                intestazioni[nome] = (intestazioni[nome] + "; " + valore) if nome == "Cookie" and nome in intestazioni else valore
            percorso = ambito.get("path", "/")
            radice = ambito.get("root_path", "")
            if radice and percorso.startswith(radice):              # montata sotto un prefisso (per esempio dentro FastAPI): le rotte non lo vedono
                percorso = percorso[len(radice):] or "/"
            query = _url.parse_qs(ambito.get("query_string", b"").decode("latin-1"), keep_blank_values=True)
            richiesta = Richiesta(ambito.get("method", "GET"), percorso, query, intestazioni, corpo, (ambito.get("client") or [""])[0])
            richiesta.https = ambito.get("scheme") == "https"

            def lavora():
                if troppo_grande:
                    return app._risposta_diretta(richiesta, 413, "Richiesta troppo grande")
                return app.risposta_a(richiesta)
            risposta = await _asincrono.to_thread(lavora)
            uscita, invia_corpo = app._uscita(richiesta, risposta)
            await invia({"type": "http.response.start", "status": risposta.stato,
                         "headers": [(k.lower().encode("latin-1"), v.encode("latin-1")) for k, v in uscita]})
            if invia_corpo:
                pezzi = risposta.blocchi()
                while True:
                    pezzo = await _asincrono.to_thread(next, pezzi, None)
                    if pezzo is None:
                        break
                    await invia({"type": "http.response.body", "body": pezzo, "more_body": True})
            await invia({"type": "http.response.body", "body": b""})
        return applicazione


class _ServerProduzione:
    """Un server waitress acceso in sottofondo (per le prove)."""

    def __init__(self, server, filo, app):
        self._server = server
        self._filo = filo
        self._app = app
        self.porta = server.effective_port
        self.indirizzo = f"http://127.0.0.1:{self.porta}"

    def ferma(self):
        self._server.close()
        self._filo.join(10)
        for funzione in self._app._alla_chiusura:
            funzione()

    def __enter__(self):
        return self

    def __exit__(self, *errori):
        self.ferma()


class ServerAvviato:
    """Un server acceso in sottofondo da Applicazione.avvia_in_sottofondo."""

    def __init__(self, server, filo, schema="http", app=None):
        self._server = server
        self._filo = filo
        self._app = app
        self.porta = server.server_address[1]
        self.indirizzo = f"{schema}://127.0.0.1:{self.porta}"

    def ferma(self):
        self._server.shutdown()
        self._server.server_close()
        self._filo.join(3)
        if self._app is not None:
            for funzione in self._app._alla_chiusura:
                funzione()

    def __enter__(self):
        return self

    def __exit__(self, *errori):
        self.ferma()


class ClienteProva:
    """Un browser finto per le prove: ricorda i cookie tra una richiesta e l'altra. Si ottiene con app.cliente().

        c = app.cliente()
        c.invia("/accedi", form={"nome": "ada", "password": "segreta"})     # il cookie di sessione si ricorda da solo
        c.ottieni("/profilo").stato                                         # 200 solo se l'accesso e' riuscito
    I metodi ritornano la Risposta; con segui=Vero seguono i reindirizzamenti."""

    def __init__(self, app):
        self.app = app
        self.cookie = {}

    def richiedi(self, metodo, percorso, json=None, form=None, intestazioni=None, file=None, segui=False, **altro):
        risposta = self.app.simula(percorso, metodo, json=json, form=form, intestazioni=intestazioni, cookie=self.cookie, file=file, **altro)
        for nome, valore in risposta.cookie_impostati.items():
            if any("max-age=0" in c.lower() for c in risposta.cookie if c.startswith(nome + "=")):
                self.cookie.pop(nome, None)
            else:
                self.cookie[nome] = valore
        for _ in range(5):
            if not segui or risposta.stato not in (301, 302, 303, 307, 308) or "Location" not in risposta.intestazioni:
                break
            risposta = self.richiedi("GET", risposta.intestazioni["Location"])
        return risposta

    def ottieni(self, percorso, **k):
        return self.richiedi("GET", percorso, **k)

    def invia(self, percorso, **k):
        return self.richiedi("POST", percorso, **k)

    def elimina(self, percorso, **k):
        return self.richiedi("DELETE", percorso, **k)

    @property
    def sessione(self):
        """Il contenuto attuale del cookie di sessione (per controllare cosa ricorda il sito)."""
        richiesta = Richiesta("GET", "/", {}, {"Cookie": "; ".join(f"{k}={v}" for k, v in self.cookie.items())}, b"", "simulato")
        return self.app._leggi_sessione(richiesta)

    def imposta_sessione(self, **dati):
        """Scrive direttamente nella sessione (per provare una pagina riservata senza passare dall'accesso)."""
        attuale = self.sessione
        attuale.update(dati)
        self.cookie[NOME_COOKIE_SESSIONE] = self.app._cookie_di_sessione(attuale)

    @property
    def token_csrf(self):
        """Il codice CSRF della sessione attuale (se ce n'e' uno: lo crea la prima pagina che lo chiede)."""
        return self.sessione.get("_csrf")


# =====================================================================================================
#  Documentazione automatica
# =====================================================================================================
def _schema(tipo):
    origine = _tipi.get_origin(tipo)
    argomenti = _tipi.get_args(tipo)
    if origine is _tipi.Union:
        altri = [a for a in argomenti if a is not type(None)]
        schema = _schema(altri[0]) if altri else {}
        schema = dict(schema)
        if type(None) in argomenti:
            schema["nullable"] = True
        return schema
    if origine in (list, _tipi.List) or tipo is list:
        return {"type": "array", "items": _schema(argomenti[0]) if argomenti else {}}
    if tipo is bool:
        return {"type": "boolean"}
    if tipo is int:
        return {"type": "integer"}
    if tipo is float:
        return {"type": "number"}
    if tipo is str:
        return {"type": "string"}
    if tipo is dict or origine is dict:
        return {"type": "object"}
    if isinstance(tipo, type) and issubclass(tipo, Modello):
        proprieta, obbligatori = {}, []
        for nome, (t, predefinito) in tipo.campi().items():
            proprieta[nome] = _schema(t)
            if predefinito is _OBBLIGATORIO:
                obbligatori.append(nome)
            elif isinstance(predefinito, (str, int, float, bool)):
                proprieta[nome]["default"] = predefinito
        schema = {"type": "object", "properties": proprieta}
        if obbligatori:
            schema["required"] = obbligatori
        return schema
    return {}


def _pagina_documentazione(descrizione, percorso):
    righe = []
    for indirizzo, metodi in descrizione["paths"].items():
        for metodo, operazione in metodi.items():
            parametri = "".join(f"<li><code>{_html.escape(p['name'])}</code> <small>({'indirizzo' if p['in'] == 'path' else 'query'}, "
                                f"{_html.escape(p['schema'].get('type', 'qualsiasi'))}{', obbligatorio' if p['required'] else ''})</small></li>"
                                for p in operazione["parameters"])
            corpo = ""
            if "requestBody" in operazione:
                schema = operazione["requestBody"]["content"]["application/json"]["schema"]
                campi = "".join(f"<li><code>{_html.escape(k)}</code> <small>({_html.escape(v.get('type', 'qualsiasi'))}"
                                f"{', obbligatorio' if k in schema.get('required', []) else ''})</small></li>" for k, v in schema.get("properties", {}).items())
                corpo = f"<p><b>Corpo JSON</b></p><ul>{campi or '<li>un oggetto JSON</li>'}</ul>"
            righe.append(f"<section><h3><span class='m {metodo}'>{metodo.upper()}</span> <code>{_html.escape(indirizzo)}</code></h3>"
                         f"<p>{_html.escape(operazione['summary'])}</p>" + (f"<p><b>Parametri</b></p><ul>{parametri}</ul>" if parametri else "") + corpo + "</section>")
    return ("<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'>"
            f"<title>{_html.escape(descrizione['info']['title'])} - documentazione</title>"
            "<style>body{font-family:system-ui,sans-serif;max-width:52rem;margin:2rem auto;padding:0 1rem;color:#222}section{border:1px solid #d5dbe3;border-radius:8px;padding:.2rem 1rem;margin:.8rem 0}"
            ".m{display:inline-block;min-width:4.5rem;text-align:center;border-radius:4px;color:#fff;font-size:.8rem;padding:.15rem .4rem;background:#555}"
            ".m.get{background:#2e7d32}.m.post{background:#1a62d6}.m.put,.m.patch{background:#b7791f}.m.delete{background:#c62828}small{color:#666}</style>"
            f"<h1>{_html.escape(descrizione['info']['title'])}</h1><p>Versione {_html.escape(descrizione['info']['version'])} &middot; "
            "<a href='/openapi.json'>descrizione OpenAPI (JSON)</a>, utilizzabile con Swagger, Postman e simili.</p>" + "".join(righe))
