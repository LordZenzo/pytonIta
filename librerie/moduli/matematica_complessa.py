"""Modulo italiano per `cmath` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import cmath as _orig
from cmath import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

radice_quadrata = _ott(_orig, 'sqrt')
fase = _ott(_orig, 'phase')
modulo_polare = _ott(_orig, 'polar')
da_polare = _ott(_orig, 'rect')
esponenziale = _ott(_orig, 'exp')
logaritmo = _ott(_orig, 'log')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'nepero': 'e', 'infinito': 'inf', 'non_numero': 'nan', 'pigreco': 'pi'}
_AUTO_TIPI = {}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
