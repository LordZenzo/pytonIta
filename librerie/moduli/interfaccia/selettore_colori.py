"""Modulo italiano per `tkinter.colorchooser` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import tkinter.colorchooser as _orig
from tkinter.colorchooser import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

chiedi_colore = _ott(_orig, 'askcolor')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'Chooser': {'comando': 'command'}, 'Dialog': {'comando': 'command', 'mostra': 'show'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
