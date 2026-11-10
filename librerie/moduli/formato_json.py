"""Modulo italiano per `json` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import json as _orig
from json import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

carica = _ott(_orig, 'load')
carica_testo = _ott(_orig, 'loads')
scarica = _ott(_orig, 'dump')
scarica_testo = _ott(_orig, 'dumps')
ErroreDecodificaJson = _ott(_orig, 'JSONDecodeError')
DecodificatoreJson = _ott(_orig, 'JSONDecoder')
CodificatoreJson = _ott(_orig, 'JSONEncoder')

from _italiano import traduci_kw as _tr, ponte as _ponte
_O = {'rientro': 'indent', 'ordina_chiavi': 'sort_keys', 'solo_ascii': 'ensure_ascii',
      'predefinito': 'default', 'separatori': 'separators', 'hook_oggetto': 'object_hook',
      'classe': 'cls'}
for _n in ('scarica', 'scarica_testo', 'carica', 'carica_testo'):
    globals()[_n] = _tr(globals()[_n], _O)
_ponte(_orig.JSONEncoder, {'default': 'predefinito'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'JSONDecoder': {'decodifica': 'decode', 'decodifica_grezzo': 'raw_decode'}, 'JSONEncoder': {'predefinito': 'default', 'codifica': 'encode', 'elemento_separatore': 'item_separator', 'chiave_separatore': 'key_separator'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
