"""Modulo italiano per `io` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import io as _orig
from io import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

FlussoTesto = _ott(_orig, 'StringIO')
FlussoByte = _ott(_orig, 'BytesIO')
InvolucroTesto = _ott(_orig, 'TextIOWrapper')
apri = _ott(_orig, 'open')
INIZIO = _ott(_orig, 'SEEK_SET')
POSIZIONE = _ott(_orig, 'SEEK_CUR')
FINE = _ott(_orig, 'SEEK_END')
alias_tipo(_ott(_orig, 'StringIO'), {'ottieni_valore': 'getvalue'})
alias_tipo(_ott(_orig, 'BytesIO'), {'ottieni_valore': 'getvalue', 'ottieni_buffer': 'getbuffer'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'BUFFER_PREDEFINITO_DIMENSIONE': 'DEFAULT_BUFFER_SIZE', 'apri_codice': 'open_code', 'testo_codifica': 'text_encoding'}
_AUTO_TIPI = {}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
