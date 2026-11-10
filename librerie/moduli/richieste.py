"""Modulo italiano per `requests` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import requests as _orig
from requests import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

ottieni = _ott(_orig, 'get')
invia = _ott(_orig, 'post')
metti = _ott(_orig, 'put')
cancella = _ott(_orig, 'delete')
testa = _ott(_orig, 'head')
modifica = _ott(_orig, 'patch')
richiesta = _ott(_orig, 'request')
Sessione = _ott(_orig, 'Session')
ErroreRichiesta = _ott(_orig, 'RequestException')
ErroreConnessione = _ott(_orig, 'ConnectionError')
ErroreHttp = _ott(_orig, 'HTTPError')
ErroreTimeout = _ott(_orig, 'Timeout')
codici = _ott(_orig, 'codes')
Risposta = _ott(_orig, 'Response')
Richiesta = _ott(_orig, 'Request')
RichiestaPreparata = _ott(_orig, 'PreparedRequest')
_OPZ = {'parametri': 'params', 'intestazioni': 'headers', 'dati': 'data', 'tempo_massimo': 'timeout', 'autenticazione': 'auth', 'verifica': 'verify', 'segui_reindirizzamenti': 'allow_redirects', 'flusso': 'stream', 'file': 'files', 'cookie': 'cookies', 'proxy': 'proxies'}
_VAL = {}
kw_tipo(_ott(_orig, 'Session'), ['request', 'get', 'post', 'put', 'delete', 'head'], _OPZ, _VAL)
alias_tipo(_ott(_orig, 'Response'), {'testo': 'text', 'contenuto': 'content', 'codice_stato': '@status_code', 'intestazioni': '@headers', 'solleva_per_stato': 'raise_for_status', 'codifica': '@encoding', 'cookie': '@cookies', 'motivo': '@reason', 'itera_contenuto': 'iter_content', 'itera_righe': 'iter_lines', 'storia': '@history', 'riuscita': 'ok'})
alias_tipo(_ott(_orig, 'Session'), {'ottieni': 'get', 'invia': 'post', 'metti': 'put', 'cancella': 'delete', 'testa': 'head', 'richiesta': 'request', 'chiudi': 'close'})

from _italiano import traduci_kw as _tr
for _n in ('ottieni', 'invia', 'metti', 'cancella', 'testa', 'modifica', 'richiesta'):
    globals()[_n] = _tr(globals()[_n], _OPZ)

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'opzioni': 'options', 'sessione': 'session'}
_AUTO_TIPI = {'PreparedRequest': {'copia': 'copy', 'prepara': 'prepare', 'prepara_autenticazione': 'prepare_auth', 'prepara_corpo': 'prepare_body', 'prepara_contenuto_lunghezza': 'prepare_content_length', 'prepara_cookie': 'prepare_cookies', 'prepara_intestazioni': 'prepare_headers', 'prepara_ganci': 'prepare_hooks', 'prepara_metodo': 'prepare_method', 'prepara_url': 'prepare_url'}, 'Request': {'prepara': 'prepare'}, 'Response': {'chiudi': 'close', 'contenuto': 'content', 'è_reindirizza': 'is_redirect', 'itera_contenuto': 'iter_content', 'itera_linee': 'iter_lines', 'successivo': 'next', 'solleva_per_stato': 'raise_for_status', 'testo': 'text'}, 'Session': {'chiudi': 'close', 'unisci_ambiente_impostazioni': 'merge_environment_settings', 'opzioni': 'options', 'prepara_richiesta': 'prepare_request', 'invia': 'send'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
