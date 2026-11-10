"""Modulo italiano per `configparser` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import configparser as _orig
from configparser import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

AnalizzatoreConfigurazione = _ott(_orig, 'ConfigParser')
AnalizzatoreConfigurazioneGrezzo = _ott(_orig, 'RawConfigParser')
ErroreConfigurazione = _ott(_orig, 'Error')
alias_tipo(_ott(_orig, 'RawConfigParser'), {'leggi': 'read', 'leggi_testo': 'read_string', 'leggi_file': 'read_file', 'sezioni': 'sections', 'ha_sezione': 'has_section', 'ha_opzione': 'has_option', 'opzioni': 'options', 'ottieni': 'get', 'ottieni_intero': 'getint', 'ottieni_decimale': 'getfloat', 'ottieni_booleano': 'getboolean', 'scrivi': 'write', 'elementi': 'items', 'rimuovi_sezione': 'remove_section', 'rimuovi_opzione': 'remove_option', 'imposta': 'set', 'aggiungi_sezione': 'add_section'})
alias_tipo(_ott(_orig, 'ConfigParser'), {'imposta': 'set', 'aggiungi_sezione': 'add_section'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'SENZA_NOME_SEZIONE': 'UNNAMED_SECTION'}
_AUTO_TIPI = {'BasicInterpolation': {'prima_ottieni': 'before_get', 'prima_insieme': 'before_set'}, 'ConfigParser': {'aggiungi_sezione': 'add_section', 'imposta': 'set'}, 'ExtendedInterpolation': {'prima_ottieni': 'before_get', 'prima_insieme': 'before_set'}, 'Interpolation': {'prima_ottieni': 'before_get', 'prima_leggi': 'before_read', 'prima_insieme': 'before_set', 'prima_scrivi': 'before_write'}, 'ParsingError': {'aggiungi': 'append', 'combina': 'combine'}, 'RawConfigParser': {'aggiungi_sezione': 'add_section', 'predefiniti': 'defaults', 'ottieni': 'get', 'ottieni_booleano': 'getboolean', 'ottieni_intero': 'getint', 'ha_opzione': 'has_option', 'ha_sezione': 'has_section', 'elementi': 'items', 'opzioni': 'options', 'leggi': 'read', 'leggi_dizionario': 'read_dict', 'leggi_file': 'read_file', 'leggi_stringa': 'read_string', 'rimuovi_opzione': 'remove_option', 'rimuovi_sezione': 'remove_section', 'imposta': 'set', 'scrivi': 'write'}, 'SectionProxy': {'ottieni': 'get', 'nome': 'name', 'analizzatore': 'parser'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
