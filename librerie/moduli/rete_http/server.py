"""Modulo italiano per `http.server` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import http.server as _orig
from http.server import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

ServerHttp = _ott(_orig, 'HTTPServer')
ServerHttpMultiplo = _ott(_orig, 'ThreadingHTTPServer')
GestoreRichiesteHttp = _ott(_orig, 'BaseHTTPRequestHandler')
GestoreFileHttp = _ott(_orig, 'SimpleHTTPRequestHandler')
alias_tipo(_ott(_orig, 'HTTPServer'), {'servi_per_sempre': 'serve_forever', 'spegni': 'shutdown', 'chiudi_server': 'server_close', 'gestisci_richiesta': 'handle_request'})
alias_tipo(_ott(_orig, 'BaseHTTPRequestHandler'), {'invia_risposta': 'send_response', 'invia_intestazione': 'send_header', 'termina_intestazioni': 'end_headers', 'invia_errore': 'send_error', 'percorso': '@path', 'comando': '@command', 'intestazioni': '@headers', 'flusso_uscita': '@wfile', 'flusso_ingresso': '@rfile', 'indirizzo_client': '@client_address'})

def _ponte_metodi():
    for _m in ('GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'PATCH', 'OPTIONS'):
        def _crea(m):
            def _gestore(self):
                f = getattr(self, 'gestisci_' + m, None)
                if f is None:
                    return self.send_error(501, "Unsupported method (%r)" % m)
                return f()
            return _gestore
        if not hasattr(_orig.BaseHTTPRequestHandler, 'do_' + _m):
            setattr(_orig.BaseHTTPRequestHandler, 'do_' + _m, _crea(_m))


_ponte_metodi()

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'BaseHTTPRequestHandler': {'messaggio_classe': 'MessageClass', 'indirizzo_stringa': 'address_string', 'data_tempo_stringa': 'date_time_string', 'richiesta_predefinito_versione': 'default_request_version', 'fine_intestazioni': 'end_headers', 'errore_contenuto_tipo': 'error_content_type', 'errore_messaggio_formato': 'error_message_format', 'svuota_buffer_intestazioni': 'flush_headers', 'gestisci': 'handle', 'gestisci_uno_richiesta': 'handle_one_request', 'registra_data_tempo_stringa': 'log_date_time_string', 'registra_errore': 'log_error', 'registra_messaggio': 'log_message', 'registra_richiesta': 'log_request', 'analizza_richiesta': 'parse_request', 'protocollo_versione': 'protocol_version', 'invia_errore': 'send_error', 'invia_intestazione': 'send_header', 'invia_risposta': 'send_response', 'invia_risposta_solo': 'send_response_only', 'server_versione': 'server_version', 'versione_stringa': 'version_string'}, 'CGIHTTPRequestHandler': {'ha_biforca': 'have_fork', 'è_eseguibile': 'is_executable', 'è_python': 'is_python', 'invia_testa': 'send_head'}, 'HTTPServer': {'server_associa': 'server_bind'}, 'HTTPStatus': {'ERRATO_GATEWAY': 'BAD_GATEWAY', 'ERRATO_RICHIESTA': 'BAD_REQUEST', 'CREATO': 'CREATED', 'TROVATO': 'FOUND', 'GATEWAY_TEMPO_MASSIMO': 'GATEWAY_TIMEOUT', 'SERVER_INTERNO_ERRORE': 'INTERNAL_SERVER_ERROR', 'LUNGHEZZA_OBBLIGATORIO': 'LENGTH_REQUIRED', 'BLOCCATO': 'LOCKED', 'SCELTE_MULTIPLO': 'MULTIPLE_CHOICES', 'MULTI_STATO': 'MULTI_STATUS', 'NON_ESTESO': 'NOT_EXTENDED', 'NON_TROVATO': 'NOT_FOUND', 'NON_MODIFICATO': 'NOT_MODIFIED', 'NESSUN_CONTENUTO': 'NO_CONTENT', 'CONTENUTO_PARZIALE': 'PARTIAL_CONTENT', 'PROXY_AUTENTICAZIONE_OBBLIGATORIO': 'PROXY_AUTHENTICATION_REQUIRED', 'RICHIESTA_TEMPO_MASSIMO': 'REQUEST_TIMEOUT', 'REIMPOSTA_CONTENUTO': 'RESET_CONTENT', 'SERVIZIO_NON_DISPONIBILE': 'SERVICE_UNAVAILABLE', 'USA_PROXY': 'USE_PROXY', 'è_client_errore': 'is_client_error', 'è_server_errore': 'is_server_error', 'è_successo': 'is_success'}, 'SimpleHTTPRequestHandler': {'estensioni_mappa': 'extensions_map', 'indice_pagine': 'index_pages', 'elenca_cartella': 'list_directory', 'invia_testa': 'send_head', 'server_versione': 'server_version', 'trasla_percorso': 'translate_path'}, 'ThreadingHTTPServer': {'demone_fili': 'daemon_threads'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
