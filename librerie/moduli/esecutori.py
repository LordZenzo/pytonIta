"""Modulo italiano per `concurrent.futures` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import concurrent.futures as _orig
from concurrent.futures import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

EsecutoreFili = _ott(_orig, 'ThreadPoolExecutor')
EsecutoreProcessi = _ott(_orig, 'ProcessPoolExecutor')
Futuro = _ott(_orig, 'Future')
man_mano_completati = _ott(_orig, 'as_completed')
aspetta = _ott(_orig, 'wait')
ErroreTimeout = _ott(_orig, 'TimeoutError')
ErroreAnnullato = _ott(_orig, 'CancelledError')
PRIMO_COMPLETATO = _ott(_orig, 'FIRST_COMPLETED')
TUTTI_COMPLETATI = _ott(_orig, 'ALL_COMPLETED')
PRIMA_ECCEZIONE = _ott(_orig, 'FIRST_EXCEPTION')
Esecutore = _ott(_orig, 'Executor')
alias_tipo(_ott(_orig, 'Executor'), {'invia': 'submit', 'mappa': 'map', 'spegni': 'shutdown'})
alias_tipo(_ott(_orig, 'Future'), {'risultato': 'result', 'eccezione': 'exception', 'annulla': 'cancel', 'è_completato': 'done', 'è_annullato': 'cancelled', 'in_esecuzione': 'running', 'aggiungi_richiamo': 'add_done_callback'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'Executor': {'mappa': 'map'}, 'Future': {'annulla': 'cancel', 'eccezione': 'exception', 'risultato': 'result', 'imposta_eccezione': 'set_exception', 'imposta_risultato': 'set_result'}, 'ProcessPoolExecutor': {'mappa': 'map'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
