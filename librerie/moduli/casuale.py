"""Modulo italiano per `random` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import random as _orig
from random import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

scelta = _ott(_orig, 'choice')
scelte = _ott(_orig, 'choices')
intero_casuale = _ott(_orig, 'randint')
intervallo_casuale = _ott(_orig, 'randrange')
mescola = _ott(_orig, 'shuffle')
campione = _ott(_orig, 'sample')
decimale_casuale = _ott(_orig, 'random')
uniforme = _ott(_orig, 'uniform')
imposta_seme = _ott(_orig, 'seed')
gaussiana = _ott(_orig, 'gauss')
normale = _ott(_orig, 'normalvariate')
triangolare = _ott(_orig, 'triangular')
bit_casuali = _ott(_orig, 'getrandbits')
byte_casuali = _ott(_orig, 'randbytes')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'Random': {'VERSIONE': 'VERSION'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
