"""Modulo italiano per `ftplib` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import ftplib as _orig
from ftplib import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

Ftp = _ott(_orig, 'FTP')
FtpSicuro = _ott(_orig, 'FTP_TLS')
ErroreFtp = _ott(_orig, 'all_errors')
alias_tipo(_ott(_orig, 'FTP'), {'accedi': 'login', 'elenca_cartella': 'nlst', 'elenco': 'dir', 'cambia_cartella': 'cwd', 'scarica_binario': 'retrbinary', 'scarica_righe': 'retrlines', 'invia_binario': 'storbinary', 'invia_righe': 'storlines', 'cancella': 'delete', 'rinomina': 'rename', 'crea_cartella': 'mkd', 'rimuovi_cartella': 'rmd', 'esci': 'quit', 'chiudi': 'close', 'cartella_corrente': 'pwd', 'dimensione': 'size'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'FTP': {'chiudi': 'close', 'connetti': 'connect', 'cartella_corrente': 'cwd', 'cancella': 'delete', 'cartella': 'dir', 'accedi': 'login', 'porta': 'port', 'esci': 'quit', 'rinomina': 'rename', 'imposta_livello_debug': 'set_debuglevel', 'dimensione': 'size', 'presa': 'sock'}, 'FTP_TLS': {'autenticazione': 'auth', 'accedi': 'login'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
