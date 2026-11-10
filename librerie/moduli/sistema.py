"""Modulo italiano per `sys` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import sys as _orig
from sys import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

argomenti = _ott(_orig, 'argv')
percorso = _ott(_orig, 'path')
piattaforma = _ott(_orig, 'platform')
versione = _ott(_orig, 'version')
informazioni_versione = _ott(_orig, 'version_info')
ingresso_standard = _ott(_orig, 'stdin')
uscita_standard = _ott(_orig, 'stdout')
errore_standard = _ott(_orig, 'stderr')
moduli = _ott(_orig, 'modules')
eseguibile = _ott(_orig, 'executable')
ottieni_limite_ricorsione = _ott(_orig, 'getrecursionlimit')
imposta_limite_ricorsione = _ott(_orig, 'setrecursionlimit')
termina = _ott(_orig, 'exit')
dimensione_oggetto = _ott(_orig, 'getsizeof')
dimensione_massima = _ott(_orig, 'maxsize')
prefisso = _ott(_orig, 'prefix')
codifica_predefinita = _ott(_orig, 'getdefaultencoding')
eccezione_corrente = _ott(_orig, 'exc_info')
conteggio_riferimenti = _ott(_orig, 'getrefcount')
ordine_byte = _ott(_orig, 'byteorder')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'base_esegui_prefisso': 'base_exec_prefix', 'base_prefisso': 'base_prefix', 'eccezione': 'exception', 'esegui_prefisso': 'exec_prefix', 'bandiere': 'flags', 'decimale_informazione': 'float_info', 'decimale_rappresentazione_stile': 'float_repr_style', 'ottieni_intero_testo_massimo_cifre': 'get_int_max_str_digits', 'impronta_informazione': 'hash_info', 'intero_informazione': 'int_info', 'percorso_ganci': 'path_hooks', 'imposta_intero_testo_massimo_cifre': 'set_int_max_str_digits', 'filo_informazione': 'thread_info'}
_AUTO_TIPI = {}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
