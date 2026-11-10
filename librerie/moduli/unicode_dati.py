"""Modulo italiano per `unicodedata` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import unicodedata as _orig
from unicodedata import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

normalizza = _ott(_orig, 'normalize')
nome = _ott(_orig, 'name')
categoria = _ott(_orig, 'category')
cerca_nome = _ott(_orig, 'lookup')
numerico = _ott(_orig, 'numeric')
decimale = _ott(_orig, 'decimal')
direzione = _ott(_orig, 'bidirectional')
è_normalizzato = _ott(_orig, 'is_normalized')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'cifra': 'digit'}
_AUTO_TIPI = {'UCD': {'cifra': 'digit'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
