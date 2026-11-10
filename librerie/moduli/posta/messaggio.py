"""Modulo italiano per `email.message` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import email.message as _orig
from email.message import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

MessaggioEmail = _ott(_orig, 'EmailMessage')
Messaggio = _ott(_orig, 'Message')
alias_tipo(_ott(_orig, 'Message'), {'ottieni_payload': 'get_payload', 'imposta_payload': 'set_payload', 'ottieni_tipo_contenuto': 'get_content_type', 'ottieni_tipo_principale': 'get_content_maintype', 'è_multiparte': 'is_multipart', 'cammina': 'walk', 'aggiungi_intestazione': 'add_header', 'ottieni_nome_file': 'get_filename', 'ottieni_parametro': 'get_param', 'come_testo': 'as_string', 'come_byte': 'as_bytes', 'ottieni_tutti': 'get_all', 'imposta_set_caratteri': 'set_charset'})
alias_tipo(_ott(_orig, 'EmailMessage'), {'imposta_contenuto': 'set_content', 'aggiungi_allegato': 'add_attachment', 'aggiungi_alternativa': 'add_alternative', 'ottieni_contenuto': 'get_content', 'ottieni_tipo_contenuto': 'get_content_type', 'è_multiparte': 'is_multipart', 'cammina': 'walk'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'Charset': {'corpo_codifica': 'body_encode', 'ottieni_corpo_codifica': 'get_body_encoding', 'ottieni_output_set_caratteri': 'get_output_charset', 'intestazione_codifica': 'header_encode', 'intestazione_codifica_linee': 'header_encode_lines'}, 'EmailMessage': {'imposta_contenuto': 'set_content'}, 'MIMEPart': {'come_stringa': 'as_string', 'svuota': 'clear', 'svuota_contenuto': 'clear_content', 'ottieni_corpo': 'get_body', 'ottieni_contenuto': 'get_content', 'itera_parti': 'iter_parts', 'imposta_contenuto': 'set_content'}, 'Message': {'aggiungi_intestazione': 'add_header', 'come_byte': 'as_bytes', 'come_stringa': 'as_string', 'cancella_parametro': 'del_param', 'ottieni': 'get', 'ottieni_tutti': 'get_all', 'ottieni_confine': 'get_boundary', 'ottieni_set_caratteri': 'get_charset', 'ottieni_contenuto_set_caratteri': 'get_content_charset', 'ottieni_contenuto_tipo': 'get_content_type', 'ottieni_tipo_predefinito': 'get_default_type', 'ottieni_nome_file': 'get_filename', 'ottieni_parametro': 'get_param', 'ottieni_parametri': 'get_params', 'ottieni_dati_trasportati': 'get_payload', 'elementi': 'items', 'chiavi': 'keys', 'elementi_grezzo': 'raw_items', 'sostituisci_intestazione': 'replace_header', 'imposta_confine': 'set_boundary', 'imposta_set_caratteri': 'set_charset', 'imposta_tipo_predefinito': 'set_default_type', 'imposta_parametro': 'set_param', 'imposta_dati_trasportati': 'set_payload', 'imposta_grezzo': 'set_raw', 'imposta_tipo': 'set_type', 'valori': 'values', 'visita': 'walk'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
