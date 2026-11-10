"""Modulo italiano per `struct` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import struct as _orig
from struct import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

impacchetta = _ott(_orig, 'pack')
spacchetta = _ott(_orig, 'unpack')
dimensione_calcolata = _ott(_orig, 'calcsize')
impacchetta_in = _ott(_orig, 'pack_into')
spacchetta_da = _ott(_orig, 'unpack_from')
StrutturaBinaria = _ott(_orig, 'Struct')
ErroreStruttura = _ott(_orig, 'error')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'itera_spacchetta': 'iter_unpack'}
_AUTO_TIPI = {}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
