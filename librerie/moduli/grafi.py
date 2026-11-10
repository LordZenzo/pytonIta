"""Modulo italiano per `graphlib` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import graphlib as _orig
from graphlib import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

OrdinatoreTopologico = _ott(_orig, 'TopologicalSorter')
ErroreCiclo = _ott(_orig, 'CycleError')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'TopologicalSorter': {'aggiungi': 'add', 'è_attivo': 'is_active', 'prepara': 'prepare', 'ordine_statico': 'static_order'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
