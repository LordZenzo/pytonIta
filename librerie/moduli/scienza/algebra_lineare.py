"""Modulo italiano per `scipy.linalg` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import scipy.linalg as _orig
from scipy.linalg import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

inversa = _ott(_orig, 'inv')
determinante = _ott(_orig, 'det')
risolvi = _ott(_orig, 'solve')
norma = _ott(_orig, 'norm')
autovalori = _ott(_orig, 'eigvals')
decomposizione_lu = _ott(_orig, 'lu')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'blocco_diagonale': 'block_diag', 'nullo_spazio': 'null_space', 'polare': 'polar'}
_AUTO_TIPI = {}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
