"""Modulo italiano per `textwrap` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import textwrap as _orig
from textwrap import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

a_capo = _ott(_orig, 'wrap')
rimuovi_rientro = _ott(_orig, 'dedent')
rientra = _ott(_orig, 'indent')
accorcia = _ott(_orig, 'shorten')
riempi = _ott(_orig, 'fill')
AccapoTesto = _ott(_orig, 'TextWrapper')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
