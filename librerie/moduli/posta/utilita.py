"""Modulo italiano per `email.utils` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import email.utils as _orig
from email.utils import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

formatta_data = _ott(_orig, 'formatdate')
analizza_data = _ott(_orig, 'parsedate_to_datetime')
formatta_indirizzo = _ott(_orig, 'formataddr')
analizza_indirizzo = _ott(_orig, 'parseaddr')
crea_id_messaggio = _ott(_orig, 'make_msgid')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'decodifica_parametri': 'decode_params', 'formatta_data_ora': 'format_datetime'}
_AUTO_TIPI = {}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
