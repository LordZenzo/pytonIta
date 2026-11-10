"""Modulo italiano per `html.parser` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import html.parser as _orig
from html.parser import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

AnalizzatoreHtml = _ott(_orig, 'HTMLParser')
alias_tipo(_ott(_orig, 'HTMLParser'), {'alimenta': 'feed', 'chiudi': 'close', 'svuota': 'reset'})

from _italiano import ponte as _ponte
_ponte(_orig.HTMLParser, {
    'handle_starttag': 'gestisci_tag_iniziale',
    'handle_endtag': 'gestisci_tag_finale',
    'handle_startendtag': 'gestisci_tag_vuoto',
    'handle_data': 'gestisci_dati',
    'handle_comment': 'gestisci_commento',
    'handle_entityref': 'gestisci_entita',
    'handle_charref': 'gestisci_carattere'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'HTMLParser': {'chiudi': 'close', 'ottieni_tag_iniziale_testo': 'get_starttag_text', 'gestisci_commento': 'handle_comment', 'gestisci_dati': 'handle_data', 'gestisci_pigreco': 'handle_pi', 'gestisci_tag_iniziale': 'handle_starttag', 'analizza_commento': 'parse_comment', 'analizza_pigreco': 'parse_pi', 'analizza_tag_iniziale': 'parse_starttag', 'reimposta': 'reset'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
