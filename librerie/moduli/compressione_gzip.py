"""Modulo italiano per `gzip` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import gzip as _orig
from gzip import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

apri = _ott(_orig, 'open')
comprimi = _ott(_orig, 'compress')
decomprimi = _ott(_orig, 'decompress')
FileGzip = _ott(_orig, 'GzipFile')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'GzipFile': {'chiudi': 'close', 'chiuso': 'closed', 'descrittore': 'fileno', 'svuota_buffer': 'flush', 'sbircia': 'peek', 'leggi': 'read', 'leggibile': 'readable', 'leggi_riga': 'readline', 'posiziona': 'seek', 'posizionabile': 'seekable', 'posizione': 'tell', 'scrivibile': 'writable', 'scrivi': 'write'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
