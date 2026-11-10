"""Modulo italiano per `keyword` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import keyword as _orig
from keyword import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

è_parola_chiave = _ott(_orig, 'iskeyword')
elenco_parole_chiave = _ott(_orig, 'kwlist')
elenco_parole_chiave_morbide = _ott(_orig, 'softkwlist')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
