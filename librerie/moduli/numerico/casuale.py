"""Modulo italiano per `numpy.random` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import numpy.random as _orig
from numpy.random import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

uniformi = _ott(_orig, 'rand')
normali = _ott(_orig, 'randn')
interi = _ott(_orig, 'randint')
seme = _ott(_orig, 'seed')
scelta = _ott(_orig, 'choice')
mescola = _ott(_orig, 'shuffle')
permutazione = _ott(_orig, 'permutation')
uniforme = _ott(_orig, 'uniform')
normale = _ott(_orig, 'normal')
generatore = _ott(_orig, 'default_rng')
campione = _ott(_orig, 'sample')
alias_tipo(_ott(_orig, 'Generator'), {'interi': 'integers', 'uniforme': 'uniform', 'normale': 'normal', 'scelta': 'choice', 'mescola': 'shuffle', 'permutazione': 'permutation', 'casuali': 'random'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'binomiale': 'binomial', 'byte': 'bytes', 'esponenziale': 'exponential', 'ottieni_stato': 'get_state', 'logistica': 'logistic', 'negativo_binomiale': 'negative_binomial', 'potenza': 'power', 'casuale': 'random', 'casuale_campione': 'random_sample', 'imposta_stato': 'set_state', 'standard_esponenziale': 'standard_exponential', 'standard_normale': 'standard_normal'}
_AUTO_TIPI = {'BitGenerator': {'blocca': 'lock', 'casuale_grezzo': 'random_raw', 'seme_sequenza': 'seed_seq', 'genera': 'spawn', 'stato': 'state'}, 'Generator': {'binomiale': 'binomial', 'bit_generatore': 'bit_generator', 'byte': 'bytes', 'esponenziale': 'exponential', 'logistica': 'logistic', 'negativo_binomiale': 'negative_binomial', 'potenza': 'power', 'casuale': 'random', 'genera': 'spawn', 'standard_esponenziale': 'standard_exponential', 'standard_normale': 'standard_normal'}, 'MT19937': {'stato': 'state'}, 'PCG64': {'stato': 'state'}, 'PCG64DXSM': {'stato': 'state'}, 'Philox': {'stato': 'state'}, 'RandomState': {'binomiale': 'binomial', 'byte': 'bytes', 'esponenziale': 'exponential', 'ottieni_stato': 'get_state', 'logistica': 'logistic', 'negativo_binomiale': 'negative_binomial', 'potenza': 'power', 'casuale': 'random', 'casuale_campione': 'random_sample', 'imposta_stato': 'set_state', 'standard_esponenziale': 'standard_exponential', 'standard_normale': 'standard_normal'}, 'SFC64': {'stato': 'state'}, 'SeedSequence': {'entropia': 'entropy', 'genera_stato': 'generate_state', 'gruppo_lavoratori': 'pool', 'gruppo_lavoratori_dimensione': 'pool_size', 'genera': 'spawn', 'genera_chiave': 'spawn_key', 'stato': 'state'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
