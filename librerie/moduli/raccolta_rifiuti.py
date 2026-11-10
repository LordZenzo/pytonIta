"""Modulo italiano per `gc` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import gc as _orig
from gc import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

raccogli = _ott(_orig, 'collect')
abilita = _ott(_orig, 'enable')
disabilita = _ott(_orig, 'disable')
è_abilitato = _ott(_orig, 'isenabled')
statistiche = _ott(_orig, 'get_stats')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'DEBUG_STATISTICHE': 'DEBUG_STATS', 'ottieni_conteggio': 'get_count', 'ottieni_debug': 'get_debug', 'ottieni_oggetti': 'get_objects', 'imposta_debug': 'set_debug'}
_AUTO_TIPI = {}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
