"""Modulo italiano per `logging.handlers` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import logging.handlers as _orig
from logging.handlers import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

GestoreFileRotante = _ott(_orig, 'RotatingFileHandler')
GestoreFileOrario = _ott(_orig, 'TimedRotatingFileHandler')
GestoreSocket = _ott(_orig, 'SocketHandler')
GestoreSmtp = _ott(_orig, 'SMTPHandler')
GestoreHttp = _ott(_orig, 'HTTPHandler')
GestoreCoda = _ott(_orig, 'QueueHandler')
AscoltatoreCoda = _ott(_orig, 'QueueListener')
GestoreMemoria = _ott(_orig, 'MemoryHandler')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'BaseRotatingHandler': {'emetti': 'emit', 'ruota': 'rotate', 'rotazione_nome_file': 'rotation_filename'}, 'BufferingHandler': {'chiudi': 'close', 'emetti': 'emit', 'svuota_buffer': 'flush'}, 'DatagramHandler': {'crea_presa': 'makeSocket', 'invia': 'send'}, 'HTTPHandler': {'emetti': 'emit', 'ottieni_connessione': 'getConnection', 'mappa_registra_record': 'mapLogRecord'}, 'MemoryHandler': {'chiudi': 'close', 'svuota_buffer': 'flush', 'imposta_destinazione': 'setTarget'}, 'NTEventLogHandler': {'chiudi': 'close', 'emetti': 'emit', 'ottieni_evento_tipo': 'getEventType'}, 'QueueHandler': {'emetti': 'emit', 'prepara': 'prepare'}, 'QueueListener': {'gestisci': 'handle', 'prepara': 'prepare', 'avvia': 'start', 'ferma': 'stop'}, 'SMTPHandler': {'emetti': 'emit', 'ottieni_oggetto': 'getSubject'}, 'SocketHandler': {'chiudi': 'close', 'crea_presa': 'createSocket', 'emetti': 'emit', 'gestisci_errore': 'handleError', 'crea_serializza': 'makePickle', 'invia': 'send'}, 'SysLogHandler': {'REGISTRA_AUTENTICAZIONE': 'LOG_AUTH', 'REGISTRA_DEMONE': 'LOG_DAEMON', 'REGISTRA_DEBUG': 'LOG_DEBUG', 'REGISTRA_INFORMAZIONE': 'LOG_INFO', 'REGISTRA_UTENTE': 'LOG_USER', 'REGISTRA_AVVISO': 'LOG_WARNING', 'chiudi': 'close', 'crea_presa': 'createSocket', 'emetti': 'emit', 'codifica_priorita': 'encodePriority', 'mappa_priorita': 'mapPriority', 'priorita_mappa': 'priority_map', 'priorita_nomi': 'priority_names'}, 'TimedRotatingFileHandler': {'ottieni_file_in_cancella': 'getFilesToDelete'}, 'WatchedFileHandler': {'emetti': 'emit'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
