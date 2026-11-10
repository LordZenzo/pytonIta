"""Modulo italiano per `shlex` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import shlex as _orig
from shlex import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

separa = _ott(_orig, 'split')
proteggi = _ott(_orig, 'quote')
unisci = _ott(_orig, 'join')
Lessico = _ott(_orig, 'shlex')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'shlex': {'ottieni_token': 'get_token', 'estrai_sorgente': 'pop_source', 'punteggiatura_caratteri': 'punctuation_chars', 'inserisci_sorgente': 'push_source', 'inserisci_token': 'push_token', 'leggi_token': 'read_token'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
