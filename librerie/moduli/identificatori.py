"""Modulo italiano per `uuid` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import uuid as _orig
from uuid import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

uuid_casuale = _ott(_orig, 'uuid4')
uuid_da_orario = _ott(_orig, 'uuid1')
uuid_da_nome = _ott(_orig, 'uuid5')
Uuid = _ott(_orig, 'UUID')
alias_tipo(_ott(_orig, 'UUID'), {'esadecimale': 'hex', 'byte': 'bytes', 'intero': 'int'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'SPAZIO_NOMI_URL': 'NAMESPACE_URL', 'principale': 'main'}
_AUTO_TIPI = {'SafeUUID': {'sicuro': 'safe', 'sconosciuto': 'unknown', 'non_sicuro': 'unsafe'}, 'UUID': {'byte': 'bytes', 'orologio_sequenza': 'clock_seq', 'orologio_sequenza_basso': 'clock_seq_low', 'campi': 'fields', 'esadecimale': 'hex', 'intero': 'int', 'è_sicuro': 'is_safe', 'nodo': 'node', 'tempo': 'time', 'tempo_basso': 'time_low', 'variante': 'variant', 'versione': 'version'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
