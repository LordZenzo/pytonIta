"""Modulo italiano per `scipy.optimize` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import scipy.optimize as _orig
from scipy.optimize import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

minimizza = _ott(_orig, 'minimize')
adatta_curva = _ott(_orig, 'curve_fit')
radice = _ott(_orig, 'root')
risolvi_sistema = _ott(_orig, 'fsolve')
programmazione_lineare = _ott(_orig, 'linprog')
minimizza_scalare = _ott(_orig, 'minimize_scalar')
trova_radice = _ott(_orig, 'brentq')
minimi_quadrati = _ott(_orig, 'least_squares')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'linea_cerca': 'line_search', 'mostra_opzioni': 'show_options'}
_AUTO_TIPI = {'BroydenFirst': {'risolvi': 'solve'}, 'HessianUpdateStrategy': {'ottieni_matrice': 'get_matrix', 'inizializza': 'initialize', 'aggiorna': 'update'}, 'InverseJacobian': {'tipo_dati': 'dtype', 'forma': 'shape'}, 'KrylovJacobian': {'risolvi': 'solve', 'aggiorna': 'update'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
