"""Modulo italiano per `threading` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import threading as _orig
from threading import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

Filo = _ott(_orig, 'Thread')
Blocco = _ott(_orig, 'Lock')
Evento = _ott(_orig, 'Event')
Condizione = _ott(_orig, 'Condition')
Semaforo = _ott(_orig, 'Semaphore')
SemaforoLimitato = _ott(_orig, 'BoundedSemaphore')
Temporizzatore = _ott(_orig, 'Timer')
Barriera = _ott(_orig, 'Barrier')
locale = _ott(_orig, 'local')
filo_corrente = _ott(_orig, 'current_thread')
filo_principale = _ott(_orig, 'main_thread')
conta_attivi = _ott(_orig, 'active_count')
elenca_fili = _ott(_orig, 'enumerate')
identificatore = _ott(_orig, 'get_ident')
alias_tipo(_ott(_orig, 'Thread'), {'avvia': 'start', 'unisci': 'join', 'è_vivo': 'is_alive', 'nome': 'name', 'demone': 'daemon', 'identificatore': 'ident'})
alias_tipo(_ott(_orig, 'Lock'), {'acquisisci': 'acquire', 'rilascia': 'release', 'bloccato': 'locked'})
alias_tipo(_ott(_orig, 'Event'), {'imposta': 'set', 'cancella': 'clear', 'aspetta': 'wait', 'è_impostato': 'is_set'})
alias_tipo(_ott(_orig, 'Condition'), {'acquisisci': '@acquire', 'rilascia': '@release', 'aspetta': 'wait', 'notifica': 'notify', 'notifica_tutti': 'notify_all', 'attendi_condizione': 'wait_for'})
alias_tipo(_ott(_orig, 'Semaphore'), {'acquisisci': 'acquire', 'rilascia': 'release'})
alias_tipo(_ott(_orig, 'Timer'), {'annulla': 'cancel'})

from _italiano import ponte as _ponte
_ponte(_orig.Thread, {'run': 'esegui'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'TEMPO_MASSIMO_MASSIMO': 'TIMEOUT_MAX', 'pila_dimensione': 'stack_size'}
_AUTO_TIPI = {'Barrier': {'rotto': 'broken', 'reimposta': 'reset', 'aspetta': 'wait'}, 'BoundedSemaphore': {'rilascia': 'release'}, 'Condition': {'notifica': 'notify', 'notifica_tutti': 'notifyAll', 'aspetta': 'wait', 'aspetta_per': 'wait_for'}, 'Event': {'svuota': 'clear', 'è_insieme': 'isSet', 'imposta': 'set', 'aspetta': 'wait'}, 'Semaphore': {'acquisisci': 'acquire', 'rilascia': 'release'}, 'Thread': {'demone': 'daemon', 'ottieni_nome': 'getName', 'è_demone': 'isDaemon', 'unisci': 'join', 'nome': 'name', 'esegui': 'run', 'imposta_demone': 'setDaemon', 'imposta_nome': 'setName', 'avvia': 'start'}, 'Timer': {'annulla': 'cancel', 'esegui': 'run'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
