"""Modulo italiano per `time` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import time as _orig
from time import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

aspetta = _ott(_orig, 'sleep')
adesso = _ott(_orig, 'time')
orario_locale = _ott(_orig, 'localtime')
orario_utc = _ott(_orig, 'gmtime')
formatta_tempo = _ott(_orig, 'strftime')
analizza_tempo = _ott(_orig, 'strptime')
contatore_prestazioni = _ott(_orig, 'perf_counter')
contatore_monotono = _ott(_orig, 'monotonic')
ora_testo = _ott(_orig, 'ctime')
crea_tempo = _ott(_orig, 'mktime')
fuso_orario = _ott(_orig, 'timezone')
tempo_processo = _ott(_orig, 'process_time')
nanosecondi = _ott(_orig, 'time_ns')
struttura_tempo = _ott(_orig, 'struct_time')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'ottieni_orologio_informazione': 'get_clock_info', 'filo_tempo': 'thread_time'}
_AUTO_TIPI = {}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
