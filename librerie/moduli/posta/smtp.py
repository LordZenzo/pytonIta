"""Modulo italiano per `smtplib` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import smtplib as _orig
from smtplib import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

Smtp = _ott(_orig, 'SMTP')
SmtpSsl = _ott(_orig, 'SMTP_SSL')
ErroreSmtp = _ott(_orig, 'SMTPException')
alias_tipo(_ott(_orig, 'SMTP'), {'avvia_tls': 'starttls', 'accedi': 'login', 'invia_messaggio': 'send_message', 'invia_posta': 'sendmail', 'esci': 'quit', 'connetti': 'connect', 'saluta': 'ehlo', 'imposta_livello_debug': 'set_debuglevel'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'LMTP': {'connetti': 'connect', 'saluta_messaggio': 'ehlo_msg'}, 'SMTP': {'autenticazione': 'auth', 'autenticazione_accesso': 'auth_login', 'chiudi': 'close', 'connetti': 'connect', 'dati': 'data', 'livello_debug': 'debuglevel', 'porta_predefinito': 'default_port', 'saluta': 'ehlo', 'saluta_messaggio': 'ehlo_msg', 'aiuto': 'help', 'accedi': 'login', 'esci': 'quit', 'invia': 'send', 'invia_messaggio': 'send_message', 'imposta_livello_debug': 'set_debuglevel', 'presa': 'sock', 'verifica': 'verify'}, 'SMTP_SSL': {'porta_predefinito': 'default_port'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
