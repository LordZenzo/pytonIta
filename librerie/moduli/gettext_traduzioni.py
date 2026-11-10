"""Modulo italiano per `gettext` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import gettext as _orig
from gettext import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

traduci = _ott(_orig, 'gettext')
installa = _ott(_orig, 'install')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'trova': 'find'}
_AUTO_TIPI = {'GNUTranslations': {'CONTESTO': 'CONTEXT'}, 'NullTranslations': {'set_caratteri': 'charset', 'informazioni': 'info'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
