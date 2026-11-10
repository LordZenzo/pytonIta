"""Modulo italiano per `pickle` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import pickle as _orig
from pickle import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

scarica = _ott(_orig, 'dump')
scarica_in_byte = _ott(_orig, 'dumps')
carica = _ott(_orig, 'load')
carica_da_byte = _ott(_orig, 'loads')
ErroreSerializzazione = _ott(_orig, 'PickleError')
PROTOCOLLO_MASSIMO = _ott(_orig, 'HIGHEST_PROTOCOL')
PROTOCOLLO_PREDEFINITO = _ott(_orig, 'DEFAULT_PROTOCOL')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'AGGIUNGI': 'APPEND', 'COSTRUISCI': 'BUILD', 'DIZIONARIO': 'DICT', 'DUPLICA': 'DUP', 'DIZIONARIO_VUOTO': 'EMPTY_DICT', 'LISTA_VUOTO': 'EMPTY_LIST', 'INSIEME_VUOTO': 'EMPTY_SET', 'TUPLA_VUOTO': 'EMPTY_TUPLE', 'FALSO': 'FALSE', 'DECIMALE': 'FLOAT', 'RIQUADRO': 'FRAME', 'OTTIENI': 'GET', 'INTERO': 'INT', 'ELENCA': 'LIST', 'LUNGO': 'LONG', 'SEGNA': 'MARK', 'SUCCESSIVO_BUFFER': 'NEXT_BUFFER', 'NESSUNO': 'NONE', 'ESTRAI': 'POP', 'ESTRAI_SEGNA': 'POP_MARK', 'INSERISCI': 'PUT', 'SOLA_LETTURA_BUFFER': 'READONLY_BUFFER', 'RIDUCI': 'REDUCE', 'PILA_GLOBALE': 'STACK_GLOBAL', 'FERMA': 'STOP', 'STRINGA': 'STRING', 'VERO': 'TRUE', 'TUPLA': 'TUPLE'}
_AUTO_TIPI = {'PickleBuffer': {'grezzo': 'raw', 'rilascia': 'release'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
