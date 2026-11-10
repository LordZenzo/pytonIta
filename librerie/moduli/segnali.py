"""Modulo italiano per `signal` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import signal as _orig
from signal import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

imposta_gestore = _ott(_orig, 'signal')
SEGNALE_INTERRUZIONE = _ott(_orig, 'SIGINT')
SEGNALE_TERMINAZIONE = _ott(_orig, 'SIGTERM')
SEGNALE_PREDEFINITO = _ott(_orig, 'SIG_DFL')
SEGNALE_IGNORA = _ott(_orig, 'SIG_IGN')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'CTRL_INTERROMPI_EVENTO': 'CTRL_BREAK_EVENT', 'intero_predefinito_gestore': 'default_int_handler', 'solleva_segnale': 'raise_signal'}
_AUTO_TIPI = {'Signals': {'CTRL_INTERROMPI_EVENTO': 'CTRL_BREAK_EVENT'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
