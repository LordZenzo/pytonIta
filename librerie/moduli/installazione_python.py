"""Modulo italiano per `sysconfig` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import sysconfig as _orig
from sysconfig import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

ottieni_percorsi = _ott(_orig, 'get_paths')
ottieni_variabile_config = _ott(_orig, 'get_config_var')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'ottieni_percorso': 'get_path', 'ottieni_percorso_nomi': 'get_path_names', 'ottieni_piattaforma': 'get_platform', 'ottieni_python_versione': 'get_python_version'}
_AUTO_TIPI = {}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
