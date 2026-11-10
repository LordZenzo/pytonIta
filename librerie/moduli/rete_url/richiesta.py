"""Modulo italiano per `urllib.request` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import urllib.request as _orig
from urllib.request import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

apri_url = _ott(_orig, 'urlopen')
Richiesta = _ott(_orig, 'Request')
costruisci_apri = _ott(_orig, 'build_opener')
scarica_in_file = _ott(_orig, 'urlretrieve')
installa_apri = _ott(_orig, 'install_opener')
GestoreProxy = _ott(_orig, 'ProxyHandler')
url_a_percorso = _ott(_orig, 'url2pathname')
percorso_a_url = _ott(_orig, 'pathname2url')
proxy_di_sistema = _ott(_orig, 'getproxies')
alias_tipo(_ott(_orig, 'Request'), {'aggiungi_intestazione': 'add_header', 'ottieni_metodo': 'get_method', 'ottieni_url': 'get_full_url', 'ha_intestazione': 'has_header'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'AbstractDigestAuthHandler': {'ottieni_entita_digerisci': 'get_entity_digest', 'reimposta_riprova_conteggio': 'reset_retry_count'}, 'BaseHandler': {'aggiungi_genitore': 'add_parent', 'chiudi': 'close', 'gestore_ordine': 'handler_order'}, 'CacheFTPHandler': {'controlla_cache': 'check_cache', 'svuota_cache': 'clear_cache', 'imposta_tempo_massimo': 'setTimeout'}, 'DataHandler': {'dati_apri': 'data_open'}, 'FancyURLopener': {'reindirizza_interno': 'redirect_internal'}, 'FileHandler': {'file_apri': 'file_open', 'ottieni_nomi': 'get_names', 'nomi': 'names', 'apri_file_locale': 'open_local_file'}, 'HTTPBasicAuthHandler': {'autenticazione_intestazione': 'auth_header'}, 'HTTPDigestAuthHandler': {'autenticazione_intestazione': 'auth_header', 'gestore_ordine': 'handler_order'}, 'HTTPError': {'intestazioni': 'headers', 'motivo': 'reason'}, 'HTTPErrorProcessor': {'gestore_ordine': 'handler_order'}, 'HTTPPasswordMgr': {'aggiungi_password': 'add_password', 'trova_utente_password': 'find_user_password', 'riduci_uri': 'reduce_uri'}, 'HTTPPasswordMgrWithDefaultRealm': {'trova_utente_password': 'find_user_password'}, 'HTTPPasswordMgrWithPriorAuth': {'aggiungi_password': 'add_password'}, 'HTTPRedirectHandler': {'infinito_messaggio': 'inf_msg', 'reindirizza_richiesta': 'redirect_request'}, 'OpenerDirector': {'aggiungi_gestore': 'add_handler', 'chiudi': 'close', 'errore': 'error', 'apri': 'open'}, 'ProxyBasicAuthHandler': {'autenticazione_intestazione': 'auth_header'}, 'ProxyDigestAuthHandler': {'autenticazione_intestazione': 'auth_header', 'gestore_ordine': 'handler_order'}, 'ProxyHandler': {'gestore_ordine': 'handler_order', 'proxy_apri': 'proxy_open'}, 'Request': {'aggiungi_intestazione': 'add_header', 'dati': 'data', 'url_completo': 'full_url', 'ottieni_url_completo': 'get_full_url', 'ottieni_intestazione': 'get_header', 'ottieni_metodo': 'get_method', 'ha_intestazione': 'has_header', 'ha_proxy': 'has_proxy', 'intestazione_elementi': 'header_items', 'rimuovi_intestazione': 'remove_header', 'imposta_proxy': 'set_proxy'}, 'URLopener': {'pulisci': 'cleanup', 'chiudi': 'close', 'apri': 'open', 'apri_dati': 'open_data', 'apri_file': 'open_file', 'apri_file_locale': 'open_local_file', 'apri_sconosciuto': 'open_unknown', 'apri_sconosciuto_proxy': 'open_unknown_proxy', 'versione': 'version'}, 'UnknownHandler': {'sconosciuto_apri': 'unknown_open'}, 'addclosehook': {'chiudi': 'close'}, 'addinfourl': {'ottieni_url': 'geturl', 'stato': 'status'}, 'ftpwrapper': {'chiudi': 'close', 'file_chiudi': 'file_close', 'inizializza': 'init', 'reale_chiudi': 'real_close'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
