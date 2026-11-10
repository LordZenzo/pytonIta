"""Modulo italiano per `os.path` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import os.path as _orig
from os.path import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

esiste = _ott(_orig, 'exists')
è_file = _ott(_orig, 'isfile')
è_cartella = _ott(_orig, 'isdir')
unisci = _ott(_orig, 'join')
dividi = _ott(_orig, 'split')
dividi_estensione = _ott(_orig, 'splitext')
nome_base = _ott(_orig, 'basename')
nome_cartella = _ott(_orig, 'dirname')
assoluto = _ott(_orig, 'abspath')
normalizza = _ott(_orig, 'normpath')
dimensione = _ott(_orig, 'getsize')
modifica_tempo = _ott(_orig, 'getmtime')
creazione_tempo = _ott(_orig, 'getctime')
espandi_utente = _ott(_orig, 'expanduser')
espandi_variabili = _ott(_orig, 'expandvars')
relativo = _ott(_orig, 'relpath')
è_assoluto = _ott(_orig, 'isabs')
percorso_reale = _ott(_orig, 'realpath')
è_collegamento = _ott(_orig, 'islink')
prefisso_comune = _ott(_orig, 'commonpath')
stesso_file = _ott(_orig, 'samefile')
dividi_unità = _ott(_orig, 'splitdrive')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
