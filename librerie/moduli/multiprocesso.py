"""Modulo italiano per `multiprocessing` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import multiprocessing as _orig
from multiprocessing import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

Processo = _ott(_orig, 'Process')
GruppoProcessi = _ott(_orig, 'Pool')
Coda = _ott(_orig, 'Queue')
CodaSemplice = _ott(_orig, 'SimpleQueue')
Gestore = _ott(_orig, 'Manager')
conta_cpu = _ott(_orig, 'cpu_count')
Blocco = _ott(_orig, 'Lock')
Evento = _ott(_orig, 'Event')
Valore = _ott(_orig, 'Value')
ArrayCondiviso = _ott(_orig, 'Array')
Tubo = _ott(_orig, 'Pipe')
processo_corrente = _ott(_orig, 'current_process')
imposta_metodo_avvio = _ott(_orig, 'set_start_method')
sostegno_congelato = _ott(_orig, 'freeze_support')
Semaforo = _ott(_orig, 'Semaphore')
alias_tipo(_ott(_orig, 'Process'), {'avvia': 'start', 'unisci': 'join', 'termina': 'terminate', 'è_vivo': 'is_alive', 'uccidi': 'kill', 'nome': 'name', 'demone': 'daemon', 'codice_uscita': 'exitcode', 'pid': 'pid'})

from multiprocessing.pool import Pool as _Pool
alias_tipo(_Pool, {'mappa': 'map', 'mappa_stella': 'starmap',
    'applica_asincrono': 'apply_async', 'mappa_asincrona': 'map_async',
    'chiudi': 'close', 'unisci': 'join', 'termina': 'terminate',
    'mappa_non_ordinata': 'imap_unordered', 'mappa_pigra': 'imap'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'barriera': 'Barrier', 'condizione': 'Condition', 'array_grezzo': 'RawArray', 'valore_grezzo': 'RawValue', 'figli_attivo': 'active_children', 'ottieni_contesto': 'get_context', 'ottieni_inizio_metodo': 'get_start_method', 'registra_in_errore_standard': 'log_to_stderr', 'genitore_processo': 'parent_process', 'imposta_eseguibile': 'set_executable'}
_AUTO_TIPI = {}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
