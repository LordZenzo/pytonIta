"""Modulo italiano per `csv` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import csv as _orig
from csv import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

lettore = _ott(_orig, 'reader')
scrittore = _ott(_orig, 'writer')
LettoreDizionario = _ott(_orig, 'DictReader')
ScrittoreDizionario = _ott(_orig, 'DictWriter')
CITA_MINIMO = _ott(_orig, 'QUOTE_MINIMAL')
CITA_TUTTO = _ott(_orig, 'QUOTE_ALL')
CITA_NON_NUMERICI = _ott(_orig, 'QUOTE_NONNUMERIC')
CITA_NESSUNO = _ott(_orig, 'QUOTE_NONE')
Dialetto = _ott(_orig, 'Dialect')
ErroreCsv = _ott(_orig, 'Error')
rileva_formato = _ott(_orig, 'Sniffer')
alias_tipo(_ott(_orig, 'DictWriter'), {'scrivi_intestazione': 'writeheader', 'scrivi_riga': 'writerow', 'scrivi_righe': 'writerows'})
alias_tipo(_ott(_orig, 'DictReader'), {'nomi_campi': 'fieldnames'})

from io import StringIO as _SIO
alias_tipo(type(_orig.writer(_SIO())), {'scrivi_riga': 'writerow', 'scrivi_righe': 'writerows'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'campo_dimensione_limita': 'field_size_limit', 'ottieni_dialetto': 'get_dialect', 'registra_dialetto': 'register_dialect', 'annulla_registrazione_dialetto': 'unregister_dialect'}
_AUTO_TIPI = {'Dialect': {'delimitatore': 'delimiter'}, 'Sniffer': {'ha_intestazione': 'has_header'}, 'excel': {'delimitatore': 'delimiter'}, 'excel_tab': {'delimitatore': 'delimiter'}, 'unix_dialect': {'delimitatore': 'delimiter'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
