"""Modulo italiano per `xml.etree.ElementTree` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import xml.etree.ElementTree as _orig
from xml.etree.ElementTree import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

analizza = _ott(_orig, 'parse')
da_testo = _ott(_orig, 'fromstring')
in_testo = _ott(_orig, 'tostring')
Elemento = _ott(_orig, 'Element')
SottoElemento = _ott(_orig, 'SubElement')
AlberoXml = _ott(_orig, 'ElementTree')
ErroreXml = _ott(_orig, 'ParseError')
indenta = _ott(_orig, 'indent')
alias_tipo(_ott(_orig, 'Element'), {'trova': 'find', 'trova_tutti': 'findall', 'trova_testo': 'findtext', 'itera': 'iter', 'aggiungi': 'append', 'rimuovi': 'remove', 'ottieni': 'get', 'imposta': 'set', 'testo': 'text', 'coda': 'tail', 'etichetta': 'tag', 'attributi': 'attrib'})
alias_tipo(_ott(_orig, 'ElementTree'), {'radice': 'getroot', 'scrivi': 'write', 'trova': 'find', 'trova_tutti': 'findall'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'commento': 'Comment', 'PIGRECO': 'PI', 'VERSIONE': 'VERSION', 'scarica': 'dump', 'registra_spazio_nomi': 'register_namespace'}
_AUTO_TIPI = {'C14NWriterTarget': {'commento': 'comment', 'dati': 'data', 'fine': 'end', 'pigreco': 'pi', 'avvia': 'start'}, 'Element': {'aggiungi': 'append', 'svuota': 'clear', 'estendi': 'extend', 'trova': 'find', 'ottieni': 'get', 'inserisci': 'insert', 'elementi': 'items', 'itera': 'iter', 'chiavi': 'keys', 'rimuovi': 'remove', 'imposta': 'set', 'testo': 'text'}, 'ElementTree': {'trova': 'find', 'itera': 'iter', 'scrivi': 'write'}, 'TreeBuilder': {'chiudi': 'close', 'commento': 'comment', 'dati': 'data', 'fine': 'end', 'pigreco': 'pi', 'avvia': 'start'}, 'XMLParser': {'chiudi': 'close', 'entita': 'entity', 'svuota_buffer': 'flush', 'destinazione': 'target', 'versione': 'version'}, 'XMLPullParser': {'chiudi': 'close', 'svuota_buffer': 'flush', 'leggi_eventi': 'read_events'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
