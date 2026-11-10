"""Modulo italiano per `asyncio` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import asyncio as _orig
from asyncio import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

esegui = _ott(_orig, 'run')
aspetta = _ott(_orig, 'sleep')
raccogli = _ott(_orig, 'gather')
crea_attivita = _ott(_orig, 'create_task')
attendi_per = _ott(_orig, 'wait_for')
in_filo = _ott(_orig, 'to_thread')
Ciclo = _ott(_orig, 'AbstractEventLoop')
Attivita = _ott(_orig, 'Task')
Futuro = _ott(_orig, 'Future')
Coda = _ott(_orig, 'Queue')
CodaLifo = _ott(_orig, 'LifoQueue')
CodaPriorita = _ott(_orig, 'PriorityQueue')
Blocco = _ott(_orig, 'Lock')
Evento = _ott(_orig, 'Event')
Semaforo = _ott(_orig, 'Semaphore')
Condizione = _ott(_orig, 'Condition')
ErroreTimeout = _ott(_orig, 'TimeoutError')
ErroreAnnullato = _ott(_orig, 'CancelledError')
garantisci_futuro = _ott(_orig, 'ensure_future')
man_mano_completati = _ott(_orig, 'as_completed')
attendi_tutti = _ott(_orig, 'wait')
ottieni_ciclo = _ott(_orig, 'get_event_loop')
nuovo_ciclo = _ott(_orig, 'new_event_loop')
imposta_ciclo = _ott(_orig, 'set_event_loop')
apri_connessione = _ott(_orig, 'open_connection')
avvia_server = _ott(_orig, 'start_server')
crea_sottoprocesso_shell = _ott(_orig, 'create_subprocess_shell')
crea_sottoprocesso = _ott(_orig, 'create_subprocess_exec')
LettoreFlusso = _ott(_orig, 'StreamReader')
ScrittoreFlusso = _ott(_orig, 'StreamWriter')
proteggi = _ott(_orig, 'shield')
alias_tipo(_ott(_orig, 'AbstractEventLoop'), {'esegui_fino_al_completamento': 'run_until_complete', 'esegui_per_sempre': 'run_forever', 'ferma': 'stop', 'chiudi': 'close', 'crea_attivita': 'create_task', 'chiama_dopo': 'call_later', 'chiama_presto': 'call_soon', 'esegui_in_esecutore': 'run_in_executor'})
alias_tipo(_ott(_orig, 'Task'), {'annulla': 'cancel', 'è_completata': 'done', 'risultato': 'result'})
alias_tipo(_ott(_orig, 'Future'), {'risultato': 'result', 'imposta_risultato': 'set_result', 'imposta_eccezione': 'set_exception', 'è_completato': 'done', 'annulla': 'cancel', 'aggiungi_richiamo': 'add_done_callback'})
alias_tipo(_ott(_orig, 'Queue'), {'inserisci': 'put', 'ottieni': 'get', 'inserisci_senza_attesa': 'put_nowait', 'ottieni_senza_attesa': 'get_nowait', 'dimensione': 'qsize', 'attivita_completata': 'task_done', 'attendi_completamento': 'join'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'PRIMO_ECCEZIONE': 'FIRST_EXCEPTION', 'tutti_attivita': 'all_tasks', 'crea_immediato_attivita_fabbrica': 'create_eager_task_factory', 'attivita_corrente': 'current_task', 'immediato_attivita_fabbrica': 'eager_task_factory', 'tempo_massimo': 'timeout', 'tempo_massimo_in_punto': 'timeout_at'}
_AUTO_TIPI = {'AbstractEventLoop': {'aggiungi_lettore': 'add_reader', 'aggiungi_segnale_gestore': 'add_signal_handler', 'chiama_in_punto': 'call_at', 'chiama_eccezione_gestore': 'call_exception_handler', 'chiudi': 'close', 'crea_connessione': 'create_connection', 'crea_server': 'create_server', 'eccezione_predefinito_gestore': 'default_exception_handler', 'ottieni_debug': 'get_debug', 'ottieni_eccezione_gestore': 'get_exception_handler', 'ottieni_attivita_fabbrica': 'get_task_factory', 'è_chiuso': 'is_closed', 'rimuovi_lettore': 'remove_reader', 'rimuovi_segnale_gestore': 'remove_signal_handler', 'imposta_debug': 'set_debug', 'imposta_eccezione_gestore': 'set_exception_handler', 'imposta_attivita_fabbrica': 'set_task_factory', 'presa_accetta': 'sock_accept', 'presa_connetti': 'sock_connect', 'presa_ricevi': 'sock_recv', 'ferma': 'stop', 'tempo': 'time'}, 'AbstractServer': {'chiudi': 'close', 'ottieni_ciclo': 'get_loop', 'aspetta_chiuso': 'wait_closed'}, 'Barrier': {'rotto': 'broken', 'reimposta': 'reset'}, 'BaseEventLoop': {'chiama_in_punto': 'call_at', 'chiama_eccezione_gestore': 'call_exception_handler', 'chiudi': 'close', 'crea_connessione': 'create_connection', 'crea_server': 'create_server', 'eccezione_predefinito_gestore': 'default_exception_handler', 'ottieni_debug': 'get_debug', 'ottieni_eccezione_gestore': 'get_exception_handler', 'ottieni_attivita_fabbrica': 'get_task_factory', 'è_chiuso': 'is_closed', 'imposta_debug': 'set_debug', 'imposta_eccezione_gestore': 'set_exception_handler', 'imposta_attivita_fabbrica': 'set_task_factory', 'ferma': 'stop', 'tempo': 'time'}, 'BaseTransport': {'chiudi': 'close', 'ottieni_extra_informazione': 'get_extra_info', 'ottieni_protocollo': 'get_protocol', 'imposta_protocollo': 'set_protocol'}, 'BoundedSemaphore': {'rilascia': 'release'}, 'BufferedProtocol': {'ottieni_buffer': 'get_buffer'}, 'Condition': {'notifica': 'notify', 'notifica_tutti': 'notify_all'}, 'Event': {'svuota': 'clear', 'è_insieme': 'is_set', 'imposta': 'set'}, 'Handle': {'annulla': 'cancel', 'ottieni_contesto': 'get_context'}, 'IocpProactor': {'accetta': 'accept', 'chiudi': 'close', 'connetti': 'connect', 'ricevi': 'recv', 'seleziona': 'select', 'invia': 'send', 'imposta_ciclo': 'set_loop', 'aspetta_per_gestisci': 'wait_for_handle'}, 'Lock': {'acquisisci': 'acquire', 'bloccato': 'locked', 'rilascia': 'release'}, 'Queue': {'vuoto': 'empty', 'completo': 'full', 'ottieni': 'get', 'unisci': 'join', 'dimensione_massima': 'maxsize', 'inserisci': 'put'}, 'Runner': {'chiudi': 'close', 'ottieni_ciclo': 'get_loop'}, 'Semaphore': {'acquisisci': 'acquire', 'bloccato': 'locked', 'rilascia': 'release'}, 'Server': {'chiudi': 'close', 'ottieni_ciclo': 'get_loop', 'aspetta_chiuso': 'wait_closed'}, 'StreamReader': {'eccezione': 'exception', 'leggi': 'read', 'leggi_riga': 'readline', 'imposta_eccezione': 'set_exception'}, 'StreamWriter': {'chiudi': 'close', 'ottieni_extra_informazione': 'get_extra_info', 'aspetta_chiuso': 'wait_closed', 'scrivi': 'write'}, 'SubprocessTransport': {'ottieni_pid': 'get_pid', 'uccidi': 'kill', 'invia_segnale': 'send_signal', 'termina': 'terminate'}, 'TimerHandle': {'annulla': 'cancel'}, 'WriteTransport': {'ottieni_scrivi_buffer_limiti': 'get_write_buffer_limits', 'ottieni_scrivi_buffer_dimensione': 'get_write_buffer_size', 'imposta_scrivi_buffer_limiti': 'set_write_buffer_limits', 'scrivi': 'write'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
