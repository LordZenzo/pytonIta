"""Modulo italiano per `zoneinfo` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import zoneinfo as _orig
from zoneinfo import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

FusoOrarioNominato = _ott(_orig, 'ZoneInfo')
fusi_disponibili = _ott(_orig, 'available_timezones')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'ZoneInfo': {'svuota_cache': 'clear_cache', 'ora_legale': 'dst', 'da_file': 'from_file', 'chiave': 'key', 'nessun_cache': 'no_cache', 'scostamento_utc': 'utcoffset'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
