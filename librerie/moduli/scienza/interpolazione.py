"""Modulo italiano per `scipy.interpolate` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import scipy.interpolate as _orig
from scipy.interpolate import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

interpola_1d = _ott(_orig, 'interp1d')
spline = _ott(_orig, 'UnivariateSpline')
interpola_griglia = _ott(_orig, 'griddata')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'inserisci': 'insert'}
_AUTO_TIPI = {'Akima1DInterpolator': {'estendi': 'extend'}, 'BPoly': {'asse': 'axis', 'costruisci_veloce': 'construct_fast', 'derivata': 'derivative', 'estendi': 'extend', 'da_potenza_base': 'from_power_basis', 'integra': 'integrate'}, 'BSpline': {'asse': 'axis', 'base_elemento': 'basis_element', 'costruisci_veloce': 'construct_fast', 'derivata': 'derivative', 'da_potenza_base': 'from_power_basis', 'integra': 'integrate'}, 'BarycentricInterpolator': {'derivata': 'derivative'}, 'BivariateSpline': {'integrale': 'integral'}, 'NdBSpline': {'derivata': 'derivative'}, 'NdPPoly': {'costruisci_veloce': 'construct_fast', 'derivata': 'derivative', 'integra': 'integrate'}, 'PPoly': {'asse': 'axis', 'costruisci_veloce': 'construct_fast', 'derivata': 'derivative', 'estendi': 'extend', 'integra': 'integrate', 'radici': 'roots', 'risolvi': 'solve'}, 'RegularGridInterpolator': {'griglia': 'grid', 'valori': 'values'}, 'UnivariateSpline': {'derivata': 'derivative', 'integrale': 'integral', 'radici': 'roots', 'convalida_ingresso': 'validate_input'}, 'interp1d': {'riempi_valore': 'fill_value'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
