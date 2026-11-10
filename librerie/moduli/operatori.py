"""Modulo italiano per `operator` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import operator as _orig
from operator import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

ottieni_elemento = _ott(_orig, 'itemgetter')
ottieni_attributo = _ott(_orig, 'attrgetter')
chiama_metodo = _ott(_orig, 'methodcaller')
somma = _ott(_orig, 'add')
sottrai = _ott(_orig, 'sub')
moltiplica = _ott(_orig, 'mul')
dividi = _ott(_orig, 'truediv')
dividi_intero = _ott(_orig, 'floordiv')
modulo = _ott(_orig, 'mod')
nega = _ott(_orig, 'neg')
uguale = _ott(_orig, 'eq')
diverso = _ott(_orig, 'ne')
minore = _ott(_orig, 'lt')
minore_uguale = _ott(_orig, 'le')
maggiore = _ott(_orig, 'gt')
maggiore_uguale = _ott(_orig, 'ge')
contiene = _ott(_orig, 'contains')
potenza = _ott(_orig, 'pow')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'chiama': 'call', 'concatena': 'concat', 'conta_di': 'countOf', 'indice': 'index', 'indice_di': 'indexOf', 'inverti': 'invert', 'è_non': 'is_not', 'posizione': 'pos', 'xor_': 'xor'}
_AUTO_TIPI = {}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
