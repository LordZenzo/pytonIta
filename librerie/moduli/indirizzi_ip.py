"""Modulo italiano per `ipaddress` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import ipaddress as _orig
from ipaddress import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

indirizzo_ip = _ott(_orig, 'ip_address')
rete_ip = _ott(_orig, 'ip_network')
interfaccia_ip = _ott(_orig, 'ip_interface')
IndirizzoIPv4 = _ott(_orig, 'IPv4Address')
IndirizzoIPv6 = _ott(_orig, 'IPv6Address')
ReteIPv4 = _ott(_orig, 'IPv4Network')
ReteIPv6 = _ott(_orig, 'IPv6Network')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'IPv4Address': {'è_globale': 'is_global', 'è_collega_locale': 'is_link_local', 'è_privato': 'is_private', 'è_riservato': 'is_reserved'}, 'IPv4Network': {'è_globale': 'is_global'}, 'IPv6Address': {'è_globale': 'is_global', 'è_collega_locale': 'is_link_local', 'è_privato': 'is_private', 'è_riservato': 'is_reserved'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
