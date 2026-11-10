"""Modulo italiano per `http.client` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import http.client as _orig
from http.client import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

ConnessioneHttp = _ott(_orig, 'HTTPConnection')
ConnessioneHttps = _ott(_orig, 'HTTPSConnection')
RispostaHttp = _ott(_orig, 'HTTPResponse')
alias_tipo(_ott(_orig, 'HTTPConnection'), {'richiesta': 'request', 'ottieni_risposta': 'getresponse', 'chiudi': 'close', 'connetti': 'connect', 'imposta_livello_debug': 'set_debuglevel'})
alias_tipo(_ott(_orig, 'HTTPResponse'), {'leggi': 'read', 'ottieni_intestazione': 'getheader', 'ottieni_intestazioni': 'getheaders', 'chiudi': 'close', 'stato': '@status', 'motivo': '@reason', 'intestazioni': '@headers'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'HTTPConnection': {'apri_automatico': 'auto_open', 'chiudi': 'close', 'connetti': 'connect', 'livello_debug': 'debuglevel', 'porta_predefinito': 'default_port', 'ottieni_proxy_risposta_intestazioni': 'get_proxy_response_headers', 'richiesta': 'request', 'risposta_classe': 'response_class', 'invia': 'send', 'imposta_livello_debug': 'set_debuglevel'}, 'HTTPResponse': {'inizia': 'begin', 'chiudi': 'close', 'descrittore': 'fileno', 'svuota_buffer': 'flush', 'ottieni_url': 'geturl', 'informazioni': 'info', 'sbircia': 'peek', 'leggi': 'read', 'leggibile': 'readable', 'leggi_riga': 'readline'}, 'HTTPSConnection': {'connetti': 'connect', 'porta_predefinito': 'default_port'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
