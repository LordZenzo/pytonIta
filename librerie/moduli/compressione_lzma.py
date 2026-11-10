"""Modulo italiano per `lzma` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import lzma as _orig
from lzma import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

apri = _ott(_orig, 'open')
comprimi = _ott(_orig, 'compress')
decomprimi = _ott(_orig, 'decompress')
FileLzma = _ott(_orig, 'LZMAFile')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'CONTROLLA_NESSUNO': 'CHECK_NONE', 'CONTROLLA_SCONOSCIUTO': 'CHECK_UNKNOWN', 'FILTRA_DELTA': 'FILTER_DELTA', 'FORMATTA_AUTOMATICO': 'FORMAT_AUTO', 'FORMATTA_GREZZO': 'FORMAT_RAW', 'MODALITA_VELOCE': 'MODE_FAST', 'MODALITA_NORMALE': 'MODE_NORMAL', 'è_controlla_supportato': 'is_check_supported'}
_AUTO_TIPI = {'LZMAFile': {'chiudi': 'close', 'chiuso': 'closed', 'descrittore': 'fileno', 'modalita': 'mode', 'nome': 'name', 'sbircia': 'peek', 'leggi': 'read', 'leggibile': 'readable', 'leggi_riga': 'readline', 'posiziona': 'seek', 'posizionabile': 'seekable', 'posizione': 'tell', 'scrivibile': 'writable', 'scrivi': 'write'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
