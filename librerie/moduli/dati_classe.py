"""Modulo italiano per `dataclasses` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import dataclasses as _orig
from dataclasses import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

classe_dati = _ott(_orig, 'dataclass')
campo = _ott(_orig, 'field')
campi = _ott(_orig, 'fields')
come_dizionario = _ott(_orig, 'asdict')
come_tupla = _ott(_orig, 'astuple')
sostituisci = _ott(_orig, 'replace')
è_classe_dati = _ott(_orig, 'is_dataclass')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'Field': {'confronta': 'compare', 'predefinito': 'default', 'fabbrica_predefinito': 'default_factory', 'impronta': 'hash', 'inizializza': 'init', 'nome': 'name', 'rappresentazione': 'repr', 'tipo': 'type'}, 'InitVar': {'tipo': 'type'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
