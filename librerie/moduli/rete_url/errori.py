"""Modulo italiano per `urllib.error` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import urllib.error as _orig
from urllib.error import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

ErroreUrl = _ott(_orig, 'URLError')
ErroreHttp = _ott(_orig, 'HTTPError')
ErroreContenutoTroncato = _ott(_orig, 'ContentTooShortError')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'HTTPError': {'intestazioni': 'headers', 'motivo': 'reason'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
