"""Modulo italiano per `bisect` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import bisect as _orig
from bisect import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

bisezione = _ott(_orig, 'bisect')
bisezione_sinistra = _ott(_orig, 'bisect_left')
bisezione_destra = _ott(_orig, 'bisect_right')
inserisci_ordinato = _ott(_orig, 'insort')
inserisci_ordinato_sinistra = _ott(_orig, 'insort_left')
inserisci_ordinato_destra = _ott(_orig, 'insort_right')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
