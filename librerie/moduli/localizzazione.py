"""Modulo italiano per `locale` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import locale as _orig
from locale import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

imposta_locale = _ott(_orig, 'setlocale')
ottieni_locale = _ott(_orig, 'getlocale')
formatta_stringa = _ott(_orig, 'format_string')
valuta = _ott(_orig, 'currency')
testo_a_decimale = _ott(_orig, 'atof')
testo_a_intero = _ott(_orig, 'atoi')
LC_TUTTO = _ott(_orig, 'LC_ALL')
LC_NUMERICO = _ott(_orig, 'LC_NUMERIC')
LC_MONETARIO = _ott(_orig, 'LC_MONETARY')
LC_TEMPO = _ott(_orig, 'LC_TIME')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'CARATTERE_MASSIMO': 'CHAR_MAX', 'normalizza': 'normalize', 'testo': 'str'}
_AUTO_TIPI = {}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
