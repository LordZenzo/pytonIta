"""Modulo italiano per `enum` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import enum as _orig
from enum import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

Enumerazione = _ott(_orig, 'Enum')
EnumerazioneIntera = _ott(_orig, 'IntEnum')
Bandiera = _ott(_orig, 'Flag')
BandieraIntera = _ott(_orig, 'IntFlag')
automatico = _ott(_orig, 'auto')
unico = _ott(_orig, 'unique')
EnumerazioneTesto = _ott(_orig, 'StrEnum')
alias_tipo(_ott(_orig, 'Enum'), {'nome': 'name', 'valore': 'value'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'CONTINUO': 'CONTINUOUS', 'MANTIENI': 'KEEP', 'CON_NOME_BANDIERE': 'NAMED_FLAGS', 'RIGIDO': 'STRICT', 'UNICO': 'UNIQUE', 'bandiera_globale_rappresentazione': 'global_flag_repr', 'testo_globale': 'global_str', 'serializza_per_nome_globale': 'pickle_by_global_name'}
_AUTO_TIPI = {'Enum': {'nome': 'name', 'valore': 'value'}, 'EnumCheck': {'CONTINUO': 'CONTINUOUS', 'CON_NOME_BANDIERE': 'NAMED_FLAGS', 'UNICO': 'UNIQUE'}, 'EnumDict': {'membro_nomi': 'member_names', 'aggiorna': 'update'}, 'FlagBoundary': {'MANTIENI': 'KEEP', 'RIGIDO': 'STRICT'}, 'property': {'membro': 'member'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
