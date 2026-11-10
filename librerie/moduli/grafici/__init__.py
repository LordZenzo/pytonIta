"""Modulo italiano per `matplotlib` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import matplotlib as _orig
from matplotlib import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

usa = _ott(_orig, 'use')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'parametri_predefinito': 'defaultParams', 'ottieni_dati_percorso': 'get_data_path', 'interattivo': 'interactive', 'è_interattivo': 'is_interactive'}
_AUTO_TIPI = {'RcParams': {'copia': 'copy', 'trova_tutti': 'find_all', 'convalida': 'validate'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
