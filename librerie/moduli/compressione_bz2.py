"""Modulo italiano per `bz2` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import bz2 as _orig
from bz2 import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

apri = _ott(_orig, 'open')
comprimi = _ott(_orig, 'compress')
decomprimi = _ott(_orig, 'decompress')
FileBz2 = _ott(_orig, 'BZ2File')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'BZ2File': {'chiudi': 'close', 'chiuso': 'closed', 'descrittore': 'fileno', 'modalita': 'mode', 'nome': 'name', 'sbircia': 'peek', 'leggi': 'read', 'leggibile': 'readable', 'leggi_riga': 'readline', 'posiziona': 'seek', 'posizionabile': 'seekable', 'posizione': 'tell', 'scrivibile': 'writable', 'scrivi': 'write'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
