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

Sicurezza: per default il server ascolta solo sul tuo computer (127.0.0.1). Con ascolta="0.0.0.0" lo vede tutta la rete.
Per un sito aperto al pubblico usa un server di produzione davanti all'applicazione (vedi `app.asgi` e la guida).
"""
import ast as _ast
import asyncio as _asincrono
import base64 as _base64
import copy as _copia
import email.parser as _email_parser
import email.policy as _email_policy
import hashlib as _hashlib
import hmac as _hmac
import html as _html
import inspect as _ispeziona
import json as _json
import mimetypes as _mimetypes
import os as _os
import re as _re
import secrets as _segreti
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

    def __init__(self, stato=500, messaggio=""):
        Exception.__init__(self, messaggio)
        self.stato = stato
        self.messaggio = messaggio or _frase(stato)


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
        self.cliente = cliente
        self.https = False
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

    # ---- regolazioni
    def configura(self, chiave_segreta=None, durata_sessione=None, csrf=None, cartella_pagine=None, dimensione_massima=None, cookie_sicuro=None,
                  intestazioni_sicurezza=None):
        """Le regolazioni del sito, tutte facoltative:
          chiave_segreta: il testo con cui si firmano i cookie di sessione (tienilo riservato; senza, le sessioni durano finche' il server resta acceso);
          durata_sessione: secondi (predefinito: 14 giorni);  csrf=Vero: ogni modulo (POST...) deve rimandare il codice di richiesta.token_csrf;
          cartella_pagine: dove sono i modelli di pagina per app.mostra;  dimensione_massima: byte accettati in una richiesta;
          cookie_sicuro=Vero: i cookie viaggiano solo su HTTPS;  intestazioni_sicurezza: dizionario che sostituisce quelle predefinite."""
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
        return self

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

    def _controlla_csrf(self, richiesta, rotta):
        if not self.csrf or rotta.senza_csrf or richiesta.metodo in ("GET", "HEAD", "OPTIONS"):
            return
        atteso = richiesta.sessione.get("_csrf")
        arrivato = richiesta.form.get("csrf") or richiesta.intestazioni.get("X-CSRF-Token") or ""
        if not atteso or not _hmac.compare_digest(str(atteso), str(arrivato)):
            raise ErroreWeb(403, "Codice CSRF mancante o sbagliato: il modulo deve contenere {{ campo_csrf }} (oppure l'intestazione X-CSRF-Token)")

    def _smista(self, richiesta):
        try:
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
            return self._pagina_errore(richiesta, errore.stato, errore.messaggio)
        except Exception as errore:
            import traceback
            traceback.print_exc()
            return self._pagina_errore(richiesta, 500, "Errore nel programma: " + type(errore).__name__ + ": " + str(errore))

    def _finisci(self, richiesta, risposta):
        """Dopo la rotta: filtri, cookie di sessione e intestazioni di sicurezza."""
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
        sessione = richiesta._sessione
        if sessione is not None and (sessione.modificata):
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
        return risposta

    def risposta_a(self, richiesta):
        """Trova la rotta giusta per una richiesta e ne ricava la risposta (non scrive nulla sulla rete: si puo' provare anche da soli)."""
        richiesta._app = self
        _locale.richiesta = richiesta
        try:
            risposta = self._smista(richiesta)
        finally:
            _locale.richiesta = None
        return self._finisci(richiesta, risposta)

    # ---- provare senza rete
    def simula(self, percorso, metodo="GET", json=None, form=None, intestazioni=None, cookie=None, file=None):
        """Prova una rotta senza accendere il server e senza rete: ritorna la Risposta (stato, testo, dati, intestazioni).

            r = app.simula("/saluta/Ada")           r.stato -> 200,  r.dati -> {"messaggio": "Ciao Ada"}
            r = app.simula("/voci", "POST", json={"titolo": "pane"})
            r = app.simula("/modulo", "POST", form={"nome": "Ada"})
        Serve per imparare e per i test automatici del tuo sito. Per provare un percorso intero (accesso, sessione, cookie) usa app.cliente()."""
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
        richiesta = Richiesta(metodo.upper(), _url.unquote(parti.path), _url.parse_qs(parti.query, keep_blank_values=True), intestazioni, corpo, "simulato")
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

    def documentazione(self, percorso="/docs", titolo=None, versione="1.0"):
        """Attiva la documentazione automatica: `percorso` (pagina leggibile) e `/openapi.json` (da aprire con Swagger, Postman...)."""
        app = self

        def pagina_docs():
            return _pagina_documentazione(app.openapi(titolo, versione), percorso)

        def schema_json():
            return app.openapi(titolo, versione)
        r1 = self._aggiungi(percorso, ("GET",), pagina_docs)
        r2 = self._aggiungi("/openapi.json", ("GET",), schema_json)
        r1.nascosta = r2.nascosta = True
        self._documentazione = percorso

    # ---- server
    def _crea_server(self, porta, ascolta, certificato=None, chiave=None):
        app = self

        class Gestore(_Gestore):
            protocol_version = "HTTP/1.1"

            def _servi(self):
                inizio = _tempo.time()
                url = _url.urlsplit(self.path)
                limite = app.dimensione_massima if app.dimensione_massima is not None else DIMENSIONE_MASSIMA
                try:
                    lunghezza = int(self.headers.get("Content-Length") or 0)
                except ValueError:
                    lunghezza = 0
                if lunghezza > limite:
                    richiesta = Richiesta(self.command, _url.unquote(url.path), {}, self.headers, b"", self.client_address[0])
                    richiesta._app = app
                    risposta = app._finisci(richiesta, app._pagina_errore(richiesta, 413, "Richiesta troppo grande"))
                    self.close_connection = True
                else:
                    corpo = self.rfile.read(lunghezza) if lunghezza > 0 else b""
                    richiesta = Richiesta(self.command, _url.unquote(url.path), _url.parse_qs(url.query, keep_blank_values=True), self.headers, corpo,
                                          self.client_address[0])
                    richiesta.https = app._https
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
        if certificato:
            contesto = _ssl.SSLContext(_ssl.PROTOCOL_TLS_SERVER)
            contesto.minimum_version = _ssl.TLSVersion.TLSv1_2
            contesto.load_cert_chain(certificato, chiave)
            server.socket = contesto.wrap_socket(server.socket, server_side=True)
            self._https = True
        return server

    def avvia(self, porta=8000, ascolta="127.0.0.1", apri_browser=False, certificato=None, chiave=None):
        """Accende il server e resta qui finche' non lo spegni (Ctrl+C, oppure «Ferma» in PitStudio). Scrive l'indirizzo, cosi' si puo' cliccare.
        Con certificato="cert.pem" e chiave="chiave.pem" il sito e' in HTTPS (https://...): serve un certificato (per provare: mkcert o openssl)."""
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
        if lunghezza > limite:
            richiesta = Richiesta(ambiente.get("REQUEST_METHOD", "GET"), percorso, query, intestazioni, b"", ambiente.get("REMOTE_ADDR", ""))
            richiesta._app = self
            risposta = self._finisci(richiesta, self._pagina_errore(richiesta, 413, "Richiesta troppo grande"))
        else:
            corpo = ambiente["wsgi.input"].read(lunghezza) if lunghezza > 0 else b""
            richiesta = Richiesta(ambiente.get("REQUEST_METHOD", "GET"), percorso, query, intestazioni, corpo, ambiente.get("REMOTE_ADDR", ""))
            richiesta.https = ambiente.get("wsgi.url_scheme") == "https"
            risposta = self.risposta_a(richiesta)
        senza_corpo = richiesta.metodo == "HEAD" or risposta.stato in (204, 304)
        intestazioni_risposta = [("Cache-Control", "no-store")]
        if risposta.stato not in (204, 304):
            intestazioni_risposta += [("Content-Type", risposta.tipo), ("Content-Length", str(len(risposta.corpo)))]
        intestazioni_risposta += list(risposta.intestazioni.items()) + [("Set-Cookie", c) for c in risposta.cookie]
        avvia_risposta(f"{risposta.stato} {_frase(risposta.stato)}", intestazioni_risposta)
        if self.registro:
            print(f"{richiesta.metodo} {percorso} {risposta.stato}", flush=True)
        return [b"" if senza_corpo else risposta.corpo]

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
                    richiesta._app = app
                    return app._finisci(richiesta, app._pagina_errore(richiesta, 413, "Richiesta troppo grande"))
                return app.risposta_a(richiesta)
            risposta = await _asincrono.to_thread(lavora)
            testata = [(b"content-type", risposta.tipo.encode("latin-1")), (b"content-length", str(len(risposta.corpo)).encode()), (b"cache-control", b"no-store")]
            testata += [(k.lower().encode("latin-1"), v.encode("latin-1")) for k, v in risposta.intestazioni.items()]
            testata += [(b"set-cookie", c.encode("latin-1")) for c in risposta.cookie]
            await invia({"type": "http.response.start", "status": risposta.stato, "headers": testata})
            await invia({"type": "http.response.body", "body": b"" if richiesta.metodo == "HEAD" or risposta.stato in (204, 304) else risposta.corpo})
        return applicazione


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

    def richiedi(self, metodo, percorso, json=None, form=None, intestazioni=None, file=None, segui=False):
        risposta = self.app.simula(percorso, metodo, json=json, form=form, intestazioni=intestazioni, cookie=self.cookie, file=file)
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
