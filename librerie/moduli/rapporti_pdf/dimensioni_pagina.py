"""Modulo italiano per `reportlab.lib.pagesizes` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import reportlab.lib.pagesizes as _orig
from reportlab.lib.pagesizes import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

A4 = _ott(_orig, 'A4')
A3 = _ott(_orig, 'A3')
A5 = _ott(_orig, 'A5')
LETTERA = _ott(_orig, 'letter')
LEGALE = _ott(_orig, 'legal')
orizzontale = _ott(_orig, 'landscape')
verticale = _ott(_orig, 'portrait')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'pollice': 'inch'}
_AUTO_TIPI = {}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
