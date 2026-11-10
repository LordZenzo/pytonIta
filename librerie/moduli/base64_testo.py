"""Modulo italiano per `base64` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import base64 as _orig
from base64 import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

codifica_base64 = _ott(_orig, 'b64encode')
decodifica_base64 = _ott(_orig, 'b64decode')
codifica_base64_url = _ott(_orig, 'urlsafe_b64encode')
decodifica_base64_url = _ott(_orig, 'urlsafe_b64decode')
codifica_base32 = _ott(_orig, 'b32encode')
decodifica_base32 = _ott(_orig, 'b32decode')
codifica_base16 = _ott(_orig, 'b16encode')
decodifica_base16 = _ott(_orig, 'b16decode')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'decodifica': 'decode', 'codifica': 'encode'}
_AUTO_TIPI = {}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
