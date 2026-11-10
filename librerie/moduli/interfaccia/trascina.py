"""Modulo italiano per `tkinter.dnd` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import tkinter.dnd as _orig
from tkinter.dnd import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

trascina_inizia = _ott(_orig, 'dnd_start')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'DndHandler': {'annulla': 'cancel', 'su_movimento': 'on_motion', 'su_rilascia': 'on_release', 'radice': 'root'}, 'Icon': {'stacca': 'detach', 'sposta': 'move', 'premi': 'press'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
