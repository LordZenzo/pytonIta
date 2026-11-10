"""Modulo italiano per `codecs` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import codecs as _orig
from codecs import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

apri = _ott(_orig, 'open')
codifica = _ott(_orig, 'encode')
decodifica = _ott(_orig, 'decode')
cerca = _ott(_orig, 'lookup')
registra = _ott(_orig, 'register')
ottieni_codificatore = _ott(_orig, 'getencoder')
ottieni_decodificatore = _ott(_orig, 'getdecoder')
BOM_UTF8 = _ott(_orig, 'BOM_UTF8')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'ignora_errori': 'ignore_errors', 'registra_errore': 'register_error', 'sostituisci_errori': 'replace_errors', 'errori_rigido': 'strict_errors'}
_AUTO_TIPI = {'BufferedIncrementalDecoder': {'reimposta': 'reset'}, 'BufferedIncrementalEncoder': {'reimposta': 'reset'}, 'IncrementalDecoder': {'reimposta': 'reset'}, 'IncrementalEncoder': {'reimposta': 'reset'}, 'StreamReader': {'leggi': 'read', 'leggi_riga': 'readline', 'reimposta': 'reset', 'posiziona': 'seek'}, 'StreamReaderWriter': {'codifica': 'encoding', 'leggi': 'read', 'leggi_riga': 'readline', 'reimposta': 'reset', 'posiziona': 'seek', 'scrivi': 'write'}, 'StreamRecoder': {'dati_codifica': 'data_encoding', 'file_codifica': 'file_encoding', 'leggi': 'read', 'leggi_riga': 'readline', 'reimposta': 'reset', 'posiziona': 'seek', 'scrivi': 'write'}, 'StreamWriter': {'reimposta': 'reset', 'posiziona': 'seek', 'scrivi': 'write'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
