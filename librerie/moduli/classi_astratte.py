"""Modulo italiano per `abc` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import abc as _orig
from abc import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

ClasseAstratta = _ott(_orig, 'ABC')
MetaClasseAstratta = _ott(_orig, 'ABCMeta')
metodo_astratto = _ott(_orig, 'abstractmethod')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'ottieni_cache_token': 'get_cache_token'}
_AUTO_TIPI = {'ABCMeta': {'registra': 'register'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
