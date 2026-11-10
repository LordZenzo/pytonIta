"""Modulo italiano per `urllib.parse` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import urllib.parse as _orig
from urllib.parse import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

analizza_url = _ott(_orig, 'urlparse')
dividi_url = _ott(_orig, 'urlsplit')
unisci_url = _ott(_orig, 'urljoin')
codifica_url = _ott(_orig, 'quote')
codifica_url_piu = _ott(_orig, 'quote_plus')
decodifica_url = _ott(_orig, 'unquote')
decodifica_url_piu = _ott(_orig, 'unquote_plus')
codifica_parametri = _ott(_orig, 'urlencode')
analizza_query = _ott(_orig, 'parse_qs')
analizza_query_lista = _ott(_orig, 'parse_qsl')
componi_url = _ott(_orig, 'urlunparse')
rimuovi_frammento = _ott(_orig, 'urldefrag')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'DefragResult': {'ottieni_url': 'geturl'}, 'DefragResultBytes': {'ottieni_url': 'geturl'}, 'ParseResult': {'ottieni_url': 'geturl'}, 'ParseResultBytes': {'ottieni_url': 'geturl'}, 'SplitResult': {'ottieni_url': 'geturl'}, 'SplitResultBytes': {'ottieni_url': 'geturl'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
