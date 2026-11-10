"""Modulo italiano per `queue` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import queue as _orig
from queue import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

Coda = _ott(_orig, 'Queue')
CodaLifo = _ott(_orig, 'LifoQueue')
CodaPriorita = _ott(_orig, 'PriorityQueue')
CodaSemplice = _ott(_orig, 'SimpleQueue')
Vuota = _ott(_orig, 'Empty')
Piena = _ott(_orig, 'Full')
alias_tipo(_ott(_orig, 'Queue'), {'inserisci': 'put', 'ottieni': 'get', 'inserisci_senza_attesa': 'put_nowait', 'ottieni_senza_attesa': 'get_nowait', 'dimensione': 'qsize', 'è_vuota': 'empty', 'è_piena': 'full', 'attività_completata': 'task_done', 'attendi_completamento': 'join'})
alias_tipo(_ott(_orig, 'SimpleQueue'), {'inserisci': 'put', 'ottieni': 'get', 'inserisci_senza_attesa': 'put_nowait', 'ottieni_senza_attesa': 'get_nowait', 'dimensione': 'qsize', 'è_vuota': 'empty'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'Queue': {'vuoto': 'empty', 'completo': 'full', 'ottieni': 'get', 'unisci': 'join', 'inserisci': 'put'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
