"""Modulo italiano per `email` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import email as _orig
from email import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)


# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'messaggio_da_file_binario': 'message_from_binary_file', 'messaggio_da_byte': 'message_from_bytes', 'messaggio_da_file': 'message_from_file', 'messaggio_da_stringa': 'message_from_string'}
_AUTO_TIPI = {}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
