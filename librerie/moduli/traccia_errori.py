"""Modulo italiano per `traceback` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import traceback as _orig
from traceback import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

stampa_pila = _ott(_orig, 'print_stack')
formatta_pila = _ott(_orig, 'format_stack')
estrai_traccia = _ott(_orig, 'extract_tb')
estrai_pila = _ott(_orig, 'extract_stack')
EccezioneTraccia = _ott(_orig, 'TracebackException')
percorri_traccia = _ott(_orig, 'walk_tb')

import sys as _sys
from _italiano import traduci_errore as _t


def formatta_eccezione(*a, **k):
    return _t(_orig.format_exc(*a, **k))


def stampa_eccezione(*a, **k):
    _sys.stderr.write(formatta_eccezione())


def formatta_eccezione_completa(*a, **k):
    return [_t(r) for r in _orig.format_exception(*a, **k)]


def stampa_eccezione_completa(*a, **k):
    _sys.stderr.write("".join(formatta_eccezione_completa(*a, **k)))

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'formatta_eccezione': 'format_exc', 'formatta_eccezione_solo': 'format_exception_only', 'formatta_lista': 'format_list', 'stampa_eccezione': 'print_exc', 'stampa_ultimo': 'print_last', 'visita_pila': 'walk_stack'}
_AUTO_TIPI = {'FrameSummary': {'nome_file': 'filename', 'linea': 'line', 'locali': 'locals', 'nome': 'name'}, 'StackSummary': {'estrai': 'extract', 'formatta': 'format', 'da_lista': 'from_list'}, 'TracebackException': {'eccezione_tipo': 'exc_type', 'eccezione_tipo_testo': 'exc_type_str', 'formatta': 'format', 'formatta_eccezione_solo': 'format_exception_only', 'da_eccezione': 'from_exception', 'stampa': 'print'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
