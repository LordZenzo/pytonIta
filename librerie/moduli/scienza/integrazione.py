"""Modulo italiano per `scipy.integrate` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import scipy.integrate as _orig
from scipy.integrate import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

integra = _ott(_orig, 'quad')
risolvi_ode = _ott(_orig, 'solve_ivp')
integra_trapezi = _ott(_orig, 'trapezoid')
integra_doppio = _ott(_orig, 'dblquad')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'DOP853': {'ordine': 'order'}, 'OdeSolver': {'passo': 'step', 'passo_dimensione': 'step_size'}, 'RK23': {'NEPERO': 'E', 'ordine': 'order'}, 'RK45': {'NEPERO': 'E', 'ordine': 'order'}, 'complex_ode': {'integra': 'integrate'}, 'ode': {'integra': 'integrate'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
