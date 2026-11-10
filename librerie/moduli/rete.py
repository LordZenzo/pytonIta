"""Modulo italiano per `socket` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import socket as _orig
from socket import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

Presa = _ott(_orig, 'socket')
FAMIGLIA_INET = _ott(_orig, 'AF_INET')
FAMIGLIA_INET6 = _ott(_orig, 'AF_INET6')
TIPO_FLUSSO = _ott(_orig, 'SOCK_STREAM')
TIPO_DATAGRAMMA = _ott(_orig, 'SOCK_DGRAM')
nome_host = _ott(_orig, 'gethostname')
indirizzo_da_nome = _ott(_orig, 'gethostbyname')
info_indirizzo = _ott(_orig, 'getaddrinfo')
crea_connessione = _ott(_orig, 'create_connection')
ErroreRete = _ott(_orig, 'error')
ErroreTimeout = _ott(_orig, 'timeout')
ErroreNomeHost = _ott(_orig, 'gaierror')
SPEGNI_LETTURA = _ott(_orig, 'SHUT_RD')
SPEGNI_SCRITTURA = _ott(_orig, 'SHUT_WR')
SPEGNI_TUTTO = _ott(_orig, 'SHUT_RDWR')
LIVELLO_PRESA = _ott(_orig, 'SOL_SOCKET')
RIUSA_INDIRIZZO = _ott(_orig, 'SO_REUSEADDR')
alias_tipo(_ott(_orig, 'socket'), {'connetti': 'connect', 'associa': 'bind', 'ascolta': 'listen', 'accetta': 'accept', 'invia': 'send', 'invia_tutto': 'sendall', 'ricevi': 'recv', 'invia_a': 'sendto', 'ricevi_da': 'recvfrom', 'chiudi': 'close', 'imposta_timeout': 'settimeout', 'imposta_opzione': 'setsockopt', 'spegni': 'shutdown', 'ottieni_nome_peer': 'getpeername', 'ottieni_nome_presa': 'getsockname', 'imposta_bloccante': 'setblocking', 'crea_file': 'makefile'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'MESSAGGIO_SBIRCIA': 'MSG_PEEK', 'MESSAGGIO_TRONCA': 'MSG_TRUNC', 'PRESA_GREZZO': 'SOCK_RAW', 'crea_server': 'create_server', 'duplica': 'dup', 'errore_scheda': 'errorTab'}
_AUTO_TIPI = {'MsgFlag': {'MESSAGGIO_SBIRCIA': 'MSG_PEEK', 'MESSAGGIO_TRONCA': 'MSG_TRUNC'}, 'SocketIO': {'chiudi': 'close', 'descrittore': 'fileno', 'modalita': 'mode', 'nome': 'name', 'leggibile': 'readable', 'posizionabile': 'seekable', 'scrivibile': 'writable', 'scrivi': 'write'}, 'SocketKind': {'PRESA_GREZZO': 'SOCK_RAW'}, 'socket': {'accetta': 'accept', 'chiudi': 'close', 'stacca': 'detach', 'duplica': 'dup', 'famiglia': 'family', 'ottieni_ereditabile': 'get_inheritable', 'imposta_ereditabile': 'set_inheritable', 'tipo': 'type'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
