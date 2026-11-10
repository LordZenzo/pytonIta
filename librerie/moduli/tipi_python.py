"""Modulo italiano per `types` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import types as _orig
from types import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

SpazioNomiSemplice = _ott(_orig, 'SimpleNamespace')
TipoFunzione = _ott(_orig, 'FunctionType')
TipoMetodo = _ott(_orig, 'MethodType')
TipoModulo = _ott(_orig, 'ModuleType')
TipoGeneratore = _ott(_orig, 'GeneratorType')
TipoLambda = _ott(_orig, 'LambdaType')
TipoNessuno = _ott(_orig, 'NoneType')
ProxyMappaturaSolaLettura = _ott(_orig, 'MappingProxyType')
crea_classe = _ott(_orig, 'new_class')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'prepara_classe': 'prepare_class'}
_AUTO_TIPI = {}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
