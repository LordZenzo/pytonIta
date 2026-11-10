"""Modulo italiano per `hashlib` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import hashlib as _orig
from hashlib import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

nuovo = _ott(_orig, 'new')
algoritmi_disponibili = _ott(_orig, 'algorithms_available')
algoritmi_garantiti = _ott(_orig, 'algorithms_guaranteed')
impronta_file = _ott(_orig, 'file_digest')
pbkdf2_hmac = _ott(_orig, 'pbkdf2_hmac')
scrypt = _ott(_orig, 'scrypt')
blake2b = _ott(_orig, 'blake2b')
blake2s = _ott(_orig, 'blake2s')

alias_tipo(type(_orig.md5()), {'aggiorna': 'update', 'digerisci': 'digest',
                               'digerisci_esadecimale': 'hexdigest', 'copia': 'copy'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
