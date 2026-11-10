"""Modulo italiano per `email.mime.image` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import email.mime.image as _orig
from email.mime.image import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

ImmagineMime = _ott(_orig, 'MIMEImage')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
