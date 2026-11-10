"""Modulo italiano per `string` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import string as _orig
from string import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

lettere_ascii = _ott(_orig, 'ascii_letters')
minuscole_ascii = _ott(_orig, 'ascii_lowercase')
maiuscole_ascii = _ott(_orig, 'ascii_uppercase')
cifre = _ott(_orig, 'digits')
punteggiatura = _ott(_orig, 'punctuation')
spazi = _ott(_orig, 'whitespace')
stampabili = _ott(_orig, 'printable')
cifre_esadecimali = _ott(_orig, 'hexdigits')
cifre_ottali = _ott(_orig, 'octdigits')
capitalizza_parole = _ott(_orig, 'capwords')
Modello = _ott(_orig, 'Template')
Formattatore = _ott(_orig, 'Formatter')
alias_tipo(_ott(_orig, 'Template'), {'sostituisci': 'substitute', 'sostituisci_sicuro': 'safe_substitute'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'Formatter': {'controlla_inutilizzato_argomenti': 'check_unused_args', 'converti_campo': 'convert_field', 'formatta': 'format', 'formatta_campo': 'format_field', 'ottieni_campo': 'get_field', 'ottieni_valore': 'get_value', 'analizza': 'parse'}, 'Template': {'delimitatore': 'delimiter', 'bandiere': 'flags', 'è_valido': 'is_valid', 'modello': 'pattern'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
