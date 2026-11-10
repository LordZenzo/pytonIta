"""Modulo italiano per `doctest` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import doctest as _orig
from doctest import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

verifica_modulo = _ott(_orig, 'testmod')
verifica_file = _ott(_orig, 'testfile')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'NORMALIZZA_SPAZI': 'NORMALIZE_WHITESPACE', 'RAPPORTO_SOLO_PRIMO_FALLIMENTO': 'REPORT_ONLY_FIRST_FAILURE', 'SALTA': 'SKIP'}
_AUTO_TIPI = {'DebugRunner': {'rapporto_fallimento': 'report_failure', 'esegui': 'run'}, 'DocFileCase': {'formatta_fallimento': 'format_failure'}, 'DocTestCase': {'formatta_fallimento': 'format_failure', 'esegui_verifica': 'runTest', 'imposta_su': 'setUp', 'descrizione_corto': 'shortDescription', 'strappa_giu': 'tearDown'}, 'DocTestFinder': {'trova': 'find'}, 'DocTestParser': {'analizza': 'parse'}, 'DocTestRunner': {'unisci': 'merge', 'rapporto_fallimento': 'report_failure', 'rapporto_inizio': 'report_start', 'rapporto_successo': 'report_success', 'esegui': 'run'}, 'OutputChecker': {'controlla_output': 'check_output'}, 'SkipDocTestCase': {'imposta_su': 'setUp', 'descrizione_corto': 'shortDescription', 'verifica_salta': 'test_skip'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
