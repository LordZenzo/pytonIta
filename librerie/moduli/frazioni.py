"""Modulo italiano per `fractions` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import fractions as _orig
from fractions import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

Frazione = _ott(_orig, 'Fraction')
alias_tipo(_ott(_orig, 'Fraction'), {'numeratore': 'numerator', 'denominatore': 'denominator', 'limita_denominatore': 'limit_denominator', 'come_rapporto': 'as_integer_ratio'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'Fraction': {'come_intero_rapporto': 'as_integer_ratio', 'da_decimale': 'from_decimal', 'è_intero': 'is_integer'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
