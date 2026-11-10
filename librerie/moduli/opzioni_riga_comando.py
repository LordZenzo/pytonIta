"""Modulo italiano per `getopt` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import getopt as _orig
from getopt import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

analizza = _ott(_orig, 'getopt')
analizza_misto = _ott(_orig, 'gnu_getopt')
ErroreOpzione = _ott(_orig, 'GetoptError')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'GetoptError': {'messaggio': 'msg'}, 'error': {'messaggio': 'msg'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
