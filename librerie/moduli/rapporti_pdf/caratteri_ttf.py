"""Modulo italiano per `reportlab.pdfbase.ttfonts` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import reportlab.pdfbase.ttfonts as _orig
from reportlab.pdfbase.ttfonts import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

CarattereTrueType = _ott(_orig, 'TTFont')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'è_byte': 'isBytes', 'è_testo': 'isStr', 'impacchetta': 'pack', 'forma_testo': 'shapeStr', 'spacchetta': 'unpack'}
_AUTO_TIPI = {'ABag': {'clona': 'clone'}, 'CMapFmt2SubHeader': {'voce_conteggio': 'entryCount', 'primo_codice': 'firstCode'}, 'TTFont': {'stato': 'State', 'aggiungi_oggetti': 'addObjects', 'pdf_cursore': 'pdfScale', 'separa_stringa': 'splitString', 'stringa_larghezza': 'stringWidth', 'annulla_registrazione': 'unregister'}, 'TTFontFace': {'ottieni_carattere_larghezza': 'getCharWidth'}, 'TTFontFile': {'estrai_informazione': 'extractInfo'}, 'TTFontMaker': {'aggiungi': 'add', 'crea_flusso': 'makeStream'}, 'TTFontParser': {'somma_controllo_file': 'checksumFile', 'file_genere': 'fileKind', 'ottieni_tabella': 'get_table', 'ottieni_tabella_posizione': 'get_table_pos', 'leggi_file': 'readFile', 'leggi_intestazione': 'readHeader', 'leggi_tabella_cartella': 'readTableDirectory', 'leggi_corto': 'read_short', 'leggi_tag': 'read_tag', 'posiziona': 'seek', 'posiziona_tabella': 'seek_table', 'salta': 'skip'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
