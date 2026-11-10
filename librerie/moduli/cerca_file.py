"""Modulo italiano per `glob` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import glob as _orig
from glob import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

cerca = _ott(_orig, 'glob')
cerca_iterando = _ott(_orig, 'iglob')
proteggi = _ott(_orig, 'escape')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'trasla': 'translate'}
_AUTO_TIPI = {}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
