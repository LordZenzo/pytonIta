"""Modulo italiano per `pprint` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import pprint as _orig
from pprint import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

stampa_formattata = _ott(_orig, 'pprint')
formatta = _ott(_orig, 'pformat')
StampanteFormattata = _ott(_orig, 'PrettyPrinter')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'PrettyPrinter': {'formatta': 'format'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
