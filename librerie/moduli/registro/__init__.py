"""Modulo italiano per `logging` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import logging as _orig
from logging import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

ottieni_registratore = _ott(_orig, 'getLogger')
configura_base = _ott(_orig, 'basicConfig')
DEBUG = _ott(_orig, 'DEBUG')
INFORMAZIONE = _ott(_orig, 'INFO')
AVVISO = _ott(_orig, 'WARNING')
ERRORE = _ott(_orig, 'ERROR')
CRITICO = _ott(_orig, 'CRITICAL')
informazione = _ott(_orig, 'info')
avviso = _ott(_orig, 'warning')
errore = _ott(_orig, 'error')
critico = _ott(_orig, 'critical')
eccezione = _ott(_orig, 'exception')
Registratore = _ott(_orig, 'Logger')
Gestore = _ott(_orig, 'Handler')
GestoreFlusso = _ott(_orig, 'StreamHandler')
GestoreFile = _ott(_orig, 'FileHandler')
Formattatore = _ott(_orig, 'Formatter')
Filtro = _ott(_orig, 'Filter')
ottieni_nome_livello = _ott(_orig, 'getLevelName')
spegni = _ott(_orig, 'shutdown')
_OPZ = {'livello': 'level', 'formato': 'format', 'nome_file': 'filename', 'modo_file': 'filemode', 'formato_data': 'datefmt', 'gestori': 'handlers', 'codifica': 'encoding', 'forza': 'force', 'flusso': 'stream'}
_VAL = {}
alias_tipo(_ott(_orig, 'Logger'), {'informazione': 'info', 'avviso': 'warning', 'errore': 'error', 'critico': 'critical', 'eccezione': 'exception', 'imposta_livello': 'setLevel', 'aggiungi_gestore': 'addHandler', 'rimuovi_gestore': 'removeHandler', 'ottieni_figlio': 'getChild', 'ha_gestori': 'hasHandlers', 'registra': 'log', 'è_abilitato_per': 'isEnabledFor'})
alias_tipo(_ott(_orig, 'Handler'), {'imposta_formattatore': 'setFormatter', 'imposta_livello': 'setLevel', 'aggiungi_filtro': 'addFilter', 'chiudi': 'close'})

from _italiano import traduci_kw as _tr
configura_base = _tr(configura_base, {
    'livello': 'level', 'formato': 'format', 'nome_file': 'filename',
    'modo_file': 'filemode', 'formato_data': 'datefmt', 'gestori': 'handlers',
    'codifica': 'encoding', 'forza': 'force', 'flusso': 'stream'})
from _italiano import ponte as _ponte
_ponte(_orig.Handler, {'emit': 'emetti'})
_ponte(_orig.Formatter, {'format': 'formatta'})
_ponte(_orig.Filter, {'filter': 'filtra'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'BASE_FORMATO': 'BASIC_FORMAT', 'FATALE': 'FATAL', 'AVVISA': 'WARN', 'aggiungi_livello_nome': 'addLevelName', 'disabilita': 'disable', 'fatale': 'fatal', 'ottieni_gestore_per_nome': 'getHandlerByName', 'ottieni_gestore_nomi': 'getHandlerNames', 'ottieni_livello_nomi_mappatura': 'getLevelNamesMapping', 'ottieni_registra_record_fabbrica': 'getLogRecordFactory', 'crea_registra_record': 'makeLogRecord', 'imposta_registra_record_fabbrica': 'setLogRecordFactory', 'avvisa': 'warn'}
_AUTO_TIPI = {'BufferingFormatter': {'formatta': 'format', 'formatta_piede': 'formatFooter', 'formatta_intestazione': 'formatHeader'}, 'FileHandler': {'chiudi': 'close', 'emetti': 'emit'}, 'Filter': {'filtra': 'filter'}, 'Filterer': {'aggiungi_filtra': 'addFilter', 'filtra': 'filter', 'rimuovi_filtra': 'removeFilter'}, 'Formatter': {'tempo_predefinito_formato': 'default_time_format', 'formatta': 'format', 'formatta_eccezione': 'formatException', 'formatta_messaggio': 'formatMessage', 'formatta_pila': 'formatStack', 'formatta_tempo': 'formatTime'}, 'Handler': {'acquisisci': 'acquire', 'chiudi': 'close', 'crea_blocca': 'createLock', 'emetti': 'emit', 'svuota_buffer': 'flush', 'formatta': 'format', 'ottieni_nome': 'get_name', 'gestisci': 'handle', 'gestisci_errore': 'handleError', 'nome': 'name', 'rilascia': 'release', 'imposta_formattatore': 'setFormatter', 'imposta_livello': 'setLevel', 'imposta_nome': 'set_name'}, 'LogRecord': {'ottieni_messaggio': 'getMessage'}, 'Logger': {'aggiungi_gestore': 'addHandler', 'fatale': 'fatal', 'ottieni_figlio': 'getChild', 'ottieni_figli': 'getChildren', 'gestisci': 'handle', 'è_abilitato_per': 'isEnabledFor', 'registra': 'log', 'crea_record': 'makeRecord', 'gestore': 'manager', 'rimuovi_gestore': 'removeHandler', 'radice': 'root', 'imposta_livello': 'setLevel', 'avvisa': 'warn'}, 'LoggerAdapter': {'è_abilitato_per': 'isEnabledFor', 'registra': 'log', 'gestore': 'manager', 'nome': 'name', 'processo': 'process', 'imposta_livello': 'setLevel', 'avvisa': 'warn'}, 'Manager': {'disabilita': 'disable', 'imposta_registra_record_fabbrica': 'setLogRecordFactory'}, 'NullHandler': {'crea_blocca': 'createLock', 'emetti': 'emit', 'gestisci': 'handle'}, 'PercentStyle': {'formato_predefinito': 'default_format', 'formatta': 'format', 'convalida': 'validate', 'convalida_modello': 'validation_pattern'}, 'PlaceHolder': {'aggiungi': 'append'}, 'StrFormatStyle': {'formato_predefinito': 'default_format', 'convalida': 'validate'}, 'StreamHandler': {'emetti': 'emit', 'svuota_buffer': 'flush', 'imposta_flusso': 'setStream'}, 'StringTemplateStyle': {'formato_predefinito': 'default_format', 'convalida': 'validate'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
