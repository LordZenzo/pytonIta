"""Modulo italiano per `tempfile` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import tempfile as _orig
from tempfile import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

crea_cartella_temporanea = _ott(_orig, 'mkdtemp')
crea_file_temporaneo = _ott(_orig, 'mkstemp')
FileTemporaneo = _ott(_orig, 'TemporaryFile')
FileTemporaneoConNome = _ott(_orig, 'NamedTemporaryFile')
CartellaTemporanea = _ott(_orig, 'TemporaryDirectory')
FileTemporaneoInMemoria = _ott(_orig, 'SpooledTemporaryFile')
cartella_temporanea = _ott(_orig, 'gettempdir')
alias_tipo(_ott(_orig, 'TemporaryDirectory'), {'pulisci': 'cleanup', 'nome': '@name'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'TEMPORANEO_MASSIMO': 'TMP_MAX'}
_AUTO_TIPI = {'SpooledTemporaryFile': {'chiudi': 'close', 'chiuso': 'closed', 'stacca': 'detach', 'codifica': 'encoding', 'errori': 'errors', 'descrittore': 'fileno', 'svuota_buffer': 'flush', 'modalita': 'mode', 'nome': 'name', 'leggi': 'read', 'leggibile': 'readable', 'leggi_riga': 'readline', 'posiziona': 'seek', 'posizionabile': 'seekable', 'posizione': 'tell', 'tronca': 'truncate', 'scrivibile': 'writable', 'scrivi': 'write'}, 'TemporaryDirectory': {'pulisci': 'cleanup'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
