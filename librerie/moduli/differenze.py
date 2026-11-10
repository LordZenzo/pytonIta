"""Modulo italiano per `difflib` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import difflib as _orig
from difflib import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

ConfrontatoreSequenze = _ott(_orig, 'SequenceMatcher')
DifferenzaTesto = _ott(_orig, 'Differ')
differenze_unificate = _ott(_orig, 'unified_diff')
differenze_contesto = _ott(_orig, 'context_diff')
trova_simili = _ott(_orig, 'get_close_matches')
differenza_html = _ott(_orig, 'HtmlDiff')
confronta_righe = _ott(_orig, 'ndiff')
alias_tipo(_ott(_orig, 'SequenceMatcher'), {'rapporto': 'ratio', 'rapporto_rapido': 'quick_ratio', 'blocchi_corrispondenti': 'get_matching_blocks', 'codici_operazione': 'get_opcodes', 'imposta_sequenze': 'set_seqs'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'differenza_byte': 'diff_bytes'}
_AUTO_TIPI = {'Differ': {'confronta': 'compare'}, 'HtmlDiff': {'crea_file': 'make_file', 'crea_tabella': 'make_table'}, 'Match': {'dimensione': 'size'}, 'SequenceMatcher': {'rapporto': 'ratio'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
