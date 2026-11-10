"""Modulo italiano per `tkinter.font` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import tkinter.font as _orig
from tkinter.font import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

Carattere = _ott(_orig, 'Font')
famiglie = _ott(_orig, 'families')
nomi_caratteri = _ott(_orig, 'names')
GRASSETTO = _ott(_orig, 'BOLD')
NORMALE = _ott(_orig, 'NORMAL')
CORSIVO = _ott(_orig, 'ITALIC')
alias_tipo(_ott(_orig, 'Font'), {'misura_testo': 'measure', 'metriche': 'metrics', 'configura': 'configure', 'copia': 'copy'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'Font': {'ottieni_opzione': 'cget', 'configura': 'config', 'copia': 'copy', 'contatore': 'counter'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
