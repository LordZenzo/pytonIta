"""Modulo italiano per `functools` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import functools as _orig
from functools import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

riduci = _ott(_orig, 'reduce')
parziale = _ott(_orig, 'partial')
memorizza = _ott(_orig, 'lru_cache')
memorizza_tutto = _ott(_orig, 'cache')
confronto_a_chiave = _ott(_orig, 'cmp_to_key')
ordinamento_totale = _ott(_orig, 'total_ordering')
avvolgi = _ott(_orig, 'wraps')
aggiorna_avvolgimento = _ott(_orig, 'update_wrapper')
singolo_dispatch = _ott(_orig, 'singledispatch')
parziale_metodo = _ott(_orig, 'partialmethod')
proprietà_memorizzata = _ott(_orig, 'cached_property')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'partial': {'argomenti': 'args', 'funzione': 'func', 'parole_chiave': 'keywords'}, 'singledispatchmethod': {'registra': 'register'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
