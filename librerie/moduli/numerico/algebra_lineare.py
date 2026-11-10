"""Modulo italiano per `numpy.linalg` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import numpy.linalg as _orig
from numpy.linalg import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

inversa = _ott(_orig, 'inv')
determinante = _ott(_orig, 'det')
autovalori_e_vettori = _ott(_orig, 'eig')
autovalori = _ott(_orig, 'eigvals')
risolvi = _ott(_orig, 'solve')
norma = _ott(_orig, 'norm')
rango = _ott(_orig, 'matrix_rank')
decomposizione_svd = _ott(_orig, 'svd')
pseudo_inversa = _ott(_orig, 'pinv')
minimi_quadrati = _ott(_orig, 'lstsq')
potenza_matrice = _ott(_orig, 'matrix_power')
ErroreAlgebraLineare = _ott(_orig, 'LinAlgError')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'diagonale': 'diagonal', 'matrice_norma': 'matrix_norm', 'matrice_trasponi': 'matrix_transpose', 'traccia': 'trace', 'vettore_norma': 'vector_norm'}
_AUTO_TIPI = {}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
