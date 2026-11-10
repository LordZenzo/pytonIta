"""Modulo italiano per `mimetypes` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import mimetypes as _orig
from mimetypes import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

indovina_tipo = _ott(_orig, 'guess_type')
indovina_estensione = _ott(_orig, 'guess_extension')
indovina_tutte_estensioni = _ott(_orig, 'guess_all_extensions')
aggiungi_tipo = _ott(_orig, 'add_type')
inizializza = _ott(_orig, 'init')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'suffisso_mappa': 'suffix_map', 'tipi_mappa': 'types_map'}
_AUTO_TIPI = {'MimeTypes': {'leggi': 'read'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
