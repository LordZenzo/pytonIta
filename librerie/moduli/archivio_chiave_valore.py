"""Modulo italiano per `shelve` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import shelve as _orig
from shelve import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

apri = _ott(_orig, 'open')
Archivio = _ott(_orig, 'Shelf')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'BsdDbShelf': {'primo': 'first', 'ultimo': 'last', 'successivo': 'next', 'precedente': 'previous', 'imposta_posizione': 'set_location'}, 'DbfilenameShelf': {'svuota': 'clear'}, 'Shelf': {'chiudi': 'close', 'ottieni': 'get', 'sincrono': 'sync'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
