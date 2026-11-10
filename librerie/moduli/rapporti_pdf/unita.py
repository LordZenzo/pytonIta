"""Modulo italiano per `reportlab.lib.units` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import reportlab.lib.units as _orig
from reportlab.lib.units import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

mm = _ott(_orig, 'mm')
cm = _ott(_orig, 'cm')
pollice = _ott(_orig, 'inch')
pica = _ott(_orig, 'pica')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'in_lunghezza': 'toLength'}
_AUTO_TIPI = {}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
