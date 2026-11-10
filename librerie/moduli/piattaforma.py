"""Modulo italiano per `platform` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import platform as _orig
from platform import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

sistema = _ott(_orig, 'system')
nome_nodo = _ott(_orig, 'node')
rilascio = _ott(_orig, 'release')
versione = _ott(_orig, 'version')
macchina = _ott(_orig, 'machine')
processore = _ott(_orig, 'processor')
piattaforma = _ott(_orig, 'platform')
versione_python = _ott(_orig, 'python_version')
architettura = _ott(_orig, 'architecture')
informazioni_sistema = _ott(_orig, 'uname')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'python_costruisci': 'python_build', 'python_versione_tupla': 'python_version_tuple'}
_AUTO_TIPI = {'AndroidVer': {'dispositivo': 'device'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
