"""Modulo italiano per `fnmatch` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import fnmatch as _orig
from fnmatch import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

corrisponde = _ott(_orig, 'fnmatch')
corrisponde_maiuscole = _ott(_orig, 'fnmatchcase')
filtra = _ott(_orig, 'filter')
traduci = _ott(_orig, 'translate')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
