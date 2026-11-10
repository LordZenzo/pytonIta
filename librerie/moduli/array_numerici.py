"""Modulo italiano per `array` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import array as _orig
from array import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

array = _ott(_orig, 'array')
codici_tipo = _ott(_orig, 'typecodes')
alias_tipo(_ott(_orig, 'array'), {'aggiungi': 'append', 'estendi': 'extend', 'inserisci': 'insert', 'estrai': 'pop', 'rimuovi': 'remove', 'inverti': 'reverse', 'conta': 'count', 'indice': 'index', 'a_lista': 'tolist', 'a_byte': 'tobytes', 'da_lista': 'fromlist', 'da_byte': 'frombytes', 'codice_tipo': 'typecode'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'ArrayType': {'aggiungi': 'append', 'buffer_informazione': 'buffer_info', 'inverti_byte': 'byteswap', 'svuota': 'clear', 'conta': 'count', 'estendi': 'extend', 'da_byte': 'frombytes', 'indice': 'index', 'inserisci': 'insert', 'dimensione_elemento': 'itemsize', 'estrai': 'pop', 'rimuovi': 'remove', 'inverti': 'reverse', 'in_byte': 'tobytes', 'in_file': 'tofile', 'in_lista': 'tolist'}, 'array': {'aggiungi': 'append', 'buffer_informazione': 'buffer_info', 'inverti_byte': 'byteswap', 'svuota': 'clear', 'conta': 'count', 'estendi': 'extend', 'da_byte': 'frombytes', 'indice': 'index', 'inserisci': 'insert', 'dimensione_elemento': 'itemsize', 'estrai': 'pop', 'rimuovi': 'remove', 'inverti': 'reverse', 'in_byte': 'tobytes', 'in_file': 'tofile', 'in_lista': 'tolist'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
