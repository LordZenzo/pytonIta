"""Modulo italiano per `copy` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import copy as _orig
from copy import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

copia = _ott(_orig, 'copy')
copia_profonda = _ott(_orig, 'deepcopy')
ErroreCopia = _ott(_orig, 'Error')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'sostituisci': 'replace'}
_AUTO_TIPI = {}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
