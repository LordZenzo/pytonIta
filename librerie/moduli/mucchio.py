"""Modulo italiano per `heapq` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import heapq as _orig
from heapq import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

inserisci = _ott(_orig, 'heappush')
estrai = _ott(_orig, 'heappop')
ordina_mucchio = _ott(_orig, 'heapify')
sostituisci = _ott(_orig, 'heapreplace')
inserisci_ed_estrai = _ott(_orig, 'heappushpop')
n_maggiori = _ott(_orig, 'nlargest')
n_minori = _ott(_orig, 'nsmallest')
unisci_ordinati = _ott(_orig, 'merge')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
