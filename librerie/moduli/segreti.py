"""Modulo italiano per `secrets` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import secrets as _orig
from secrets import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

token_esadecimale = _ott(_orig, 'token_hex')
token_byte = _ott(_orig, 'token_bytes')
token_url = _ott(_orig, 'token_urlsafe')
scelta = _ott(_orig, 'choice')
casuale_sotto = _ott(_orig, 'randbelow')
confronta_sicuro = _ott(_orig, 'compare_digest')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
