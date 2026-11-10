"""Modulo italiano per `itertools` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import itertools as _orig
from itertools import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

catena = _ott(_orig, 'chain')
combinazioni = _ott(_orig, 'combinations')
combinazioni_con_ripetizione = _ott(_orig, 'combinations_with_replacement')
permutazioni = _ott(_orig, 'permutations')
prodotto_cartesiano = _ott(_orig, 'product')
ripeti = _ott(_orig, 'repeat')
accumula = _ott(_orig, 'accumulate')
ciclo = _ott(_orig, 'cycle')
conta = _ott(_orig, 'count')
fetta = _ott(_orig, 'islice')
zip_più_lungo = _ott(_orig, 'zip_longest')
raggruppa = _ott(_orig, 'groupby')
comprimi = _ott(_orig, 'compress')
prendi_mentre = _ott(_orig, 'takewhile')
salta_mentre = _ott(_orig, 'dropwhile')
copia_iteratore = _ott(_orig, 'tee')
mappa_stella = _ott(_orig, 'starmap')
a_coppie = _ott(_orig, 'pairwise')
a_blocchi = _ott(_orig, 'batched')
filtra_falsi = _ott(_orig, 'filterfalse')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'chain': {'da_iterabile': 'from_iterable'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
