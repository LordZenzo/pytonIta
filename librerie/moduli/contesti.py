"""Modulo italiano per `contextlib` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import contextlib as _orig
from contextlib import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

gestore_contesto = _ott(_orig, 'contextmanager')
chiudi_alla_fine = _ott(_orig, 'closing')
sopprimi = _ott(_orig, 'suppress')
reindirizza_uscita = _ott(_orig, 'redirect_stdout')
reindirizza_errori = _ott(_orig, 'redirect_stderr')
PilaUscite = _ott(_orig, 'ExitStack')
contesto_nullo = _ott(_orig, 'nullcontext')
gestore_contesto_asincrono = _ott(_orig, 'asynccontextmanager')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'AsyncExitStack': {'entra_contesto_asincrono': 'enter_async_context', 'inserisci_richiamo_asincrono': 'push_async_callback'}, 'ExitStack': {'chiudi': 'close'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
