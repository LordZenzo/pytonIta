"""Modulo italiano per `scipy` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import scipy as _orig
from scipy import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)


# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'mostra_configurazione': 'show_config', 'verifica': 'test'}
_AUTO_TIPI = {'LowLevelCallable': {'funzione': 'function', 'utente_dati': 'user_data'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
