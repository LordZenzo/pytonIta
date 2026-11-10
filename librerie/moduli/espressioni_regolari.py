"""Modulo italiano per `re` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import re as _orig
from re import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

cerca = _ott(_orig, 'search')
corrisponde = _ott(_orig, 'match')
corrisponde_tutto = _ott(_orig, 'fullmatch')
trova_tutti = _ott(_orig, 'findall')
trova_iterando = _ott(_orig, 'finditer')
sostituisci = _ott(_orig, 'sub')
sostituisci_conta = _ott(_orig, 'subn')
separa = _ott(_orig, 'split')
compila = _ott(_orig, 'compile')
proteggi = _ott(_orig, 'escape')
IGNORA_MAIUSCOLE = _ott(_orig, 'IGNORECASE')
MULTIRIGA = _ott(_orig, 'MULTILINE')
PUNTO_TUTTO = _ott(_orig, 'DOTALL')
VERBOSO = _ott(_orig, 'VERBOSE')
ERRORE = _ott(_orig, 'error')
Modello = _ott(_orig, 'Pattern')
Corrispondenza = _ott(_orig, 'Match')
alias_tipo(_ott(_orig, 'Pattern'), {'cerca': 'search', 'corrisponde': 'match', 'corrisponde_tutto': 'fullmatch', 'trova_tutti': 'findall', 'trova_iterando': 'finditer', 'sostituisci': 'sub', 'sostituisci_conta': 'subn', 'separa': 'split'})
alias_tipo(_ott(_orig, 'Match'), {'gruppo': 'group', 'gruppi': 'groups', 'dizionario_gruppi': 'groupdict', 'inizio': 'start', 'fine': 'end', 'intervallo': 'span'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'LOCALIZZAZIONE': 'LOCALE'}
_AUTO_TIPI = {'Match': {'fine': 'end', 'espandi': 'expand', 'raggruppa': 'group', 'gruppi': 'groups', 'posizione': 'pos', 'intervallo': 'span', 'avvia': 'start', 'stringa': 'string'}, 'Pattern': {'bandiere': 'flags', 'gruppi': 'groups', 'modello': 'pattern'}, 'RegexFlag': {'LOCALIZZAZIONE': 'LOCALE'}, 'Scanner': {'scansiona': 'scan'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
