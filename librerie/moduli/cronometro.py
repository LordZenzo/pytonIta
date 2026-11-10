"""Modulo italiano per `timeit` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import timeit as _orig
from timeit import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

misura = _ott(_orig, 'timeit')
ripeti = _ott(_orig, 'repeat')
contatore = _ott(_orig, 'default_timer')
Cronometro = _ott(_orig, 'Timer')
_OPZ = {'numero': 'number', 'ripetizioni': 'repeat', 'preparazione': 'setup', 'istruzione': 'stmt'}
_VAL = {}
alias_tipo(_ott(_orig, 'Timer'), {'misura': 'timeit', 'ripeti': 'repeat'})

from _italiano import traduci_kw as _tr
misura = _tr(misura, _OPZ)
ripeti = _tr(ripeti, _OPZ)

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'Timer': {'stampa_eccezione': 'print_exc'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
