"""Modulo italiano per `ssl` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import ssl as _orig
from ssl import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

crea_contesto_predefinito = _ott(_orig, 'create_default_context')
ContestoSsl = _ott(_orig, 'SSLContext')
ErroreSsl = _ott(_orig, 'SSLError')
VERSIONE_OPENSSL = _ott(_orig, 'OPENSSL_VERSION')
richiedi_certificato = _ott(_orig, 'CERT_REQUIRED')
nessun_certificato = _ott(_orig, 'CERT_NONE')
alias_tipo(_ott(_orig, 'SSLContext'), {'avvolgi_presa': 'wrap_socket', 'carica_catena_certificati': 'load_cert_chain', 'carica_certificati_verifica': 'load_verify_locations', 'imposta_protocolli': 'set_ciphers'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'PRESA_FLUSSO': 'SOCK_STREAM', 'VERIFICA_PREDEFINITO': 'VERIFY_DEFAULT', 'crea_connessione': 'create_connection', 'ottieni_verifica_predefinito_percorsi': 'get_default_verify_paths', 'ottieni_protocollo_nome': 'get_protocol_name'}
_AUTO_TIPI = {'Purpose': {'CLIENT_AUTENTICAZIONE': 'CLIENT_AUTH', 'SERVER_AUTENTICAZIONE': 'SERVER_AUTH'}, 'SSLContext': {'versione_massimo': 'maximum_version', 'versione_minimo': 'minimum_version', 'opzioni': 'options', 'protocollo': 'protocol', 'verifica_bandiere': 'verify_flags', 'verifica_modalita': 'verify_mode', 'avvolgi_presa': 'wrap_socket'}, 'SSLObject': {'contesto': 'context', 'leggi': 'read', 'server_nome_host': 'server_hostname', 'server_lato': 'server_side', 'sessione': 'session', 'scarta_avvolgimento': 'unwrap', 'versione': 'version', 'scrivi': 'write'}, 'SSLSocket': {'accetta': 'accept', 'connetti': 'connect', 'contesto': 'context', 'duplica': 'dup', 'leggi': 'read', 'ricevi': 'recv', 'invia': 'send', 'sessione': 'session', 'scarta_avvolgimento': 'unwrap', 'versione': 'version', 'scrivi': 'write'}, 'TLSVersion': {'SUPPORTATO_MASSIMO': 'MAXIMUM_SUPPORTED', 'SUPPORTATO_MINIMO': 'MINIMUM_SUPPORTED'}, 'VerifyFlags': {'VERIFICA_PREDEFINITO': 'VERIFY_DEFAULT'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
