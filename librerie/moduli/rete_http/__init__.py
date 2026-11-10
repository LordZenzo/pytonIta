"""Modulo italiano per `http` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import http as _orig
from http import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

StatoHttp = _ott(_orig, 'HTTPStatus')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'HTTPMethod': {'CONNETTI': 'CONNECT', 'CANCELLA': 'DELETE', 'OTTIENI': 'GET', 'TESTA': 'HEAD', 'OPZIONI': 'OPTIONS', 'TOPPA': 'PATCH', 'MOSTRA_A': 'POST', 'INSERISCI': 'PUT', 'TRACCIA': 'TRACE'}, 'HTTPStatus': {'ERRATO_GATEWAY': 'BAD_GATEWAY', 'ERRATO_RICHIESTA': 'BAD_REQUEST', 'CREATO': 'CREATED', 'TROVATO': 'FOUND', 'GATEWAY_TEMPO_MASSIMO': 'GATEWAY_TIMEOUT', 'SERVER_INTERNO_ERRORE': 'INTERNAL_SERVER_ERROR', 'LUNGHEZZA_OBBLIGATORIO': 'LENGTH_REQUIRED', 'BLOCCATO': 'LOCKED', 'SCELTE_MULTIPLO': 'MULTIPLE_CHOICES', 'MULTI_STATO': 'MULTI_STATUS', 'NON_ESTESO': 'NOT_EXTENDED', 'NON_TROVATO': 'NOT_FOUND', 'NON_MODIFICATO': 'NOT_MODIFIED', 'NESSUN_CONTENUTO': 'NO_CONTENT', 'CONTENUTO_PARZIALE': 'PARTIAL_CONTENT', 'PROXY_AUTENTICAZIONE_OBBLIGATORIO': 'PROXY_AUTHENTICATION_REQUIRED', 'RICHIESTA_TEMPO_MASSIMO': 'REQUEST_TIMEOUT', 'REIMPOSTA_CONTENUTO': 'RESET_CONTENT', 'SERVIZIO_NON_DISPONIBILE': 'SERVICE_UNAVAILABLE', 'USA_PROXY': 'USE_PROXY', 'è_client_errore': 'is_client_error', 'è_server_errore': 'is_server_error', 'è_successo': 'is_success'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
