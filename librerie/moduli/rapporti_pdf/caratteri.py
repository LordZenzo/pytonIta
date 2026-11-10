"""Modulo italiano per `reportlab.pdfbase.pdfmetrics` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import reportlab.pdfbase.pdfmetrics as _orig
from reportlab.pdfbase.pdfmetrics import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

registra_carattere = _ott(_orig, 'registerFont')
larghezza_testo = _ott(_orig, 'stringWidth')
registra_famiglia = _ott(_orig, 'registerFontFamily')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'scarica_carattere_dati': 'dumpFontData', 'trova_carattere_e_registra': 'findFontAndRegister', 'trova_in_percorsi': 'findInPaths', 'ottieni_codifica': 'getEncoding', 'ottieni_carattere': 'getFont', 'ottieni_tipo_faccia': 'getTypeFace', 'è_sequenza': 'isSeq', 'è_testo': 'isStr', 'apri_e_leggi': 'open_and_read', 'registra_codifica': 'registerEncoding', 'registra_tipo_faccia': 'registerTypeFace', 'standard_caratteri': 'standardFonts', 'verifica': 'test', 'avvisa_una_volta': 'warnOnce'}
_AUTO_TIPI = {'EmbeddedType1Face': {'aggiungi_oggetti': 'addObjects', 'ottieni_carattere_file': 'getFontFiles'}, 'Encoding': {'è_uguale': 'isEqual', 'crea_pdf_oggetto': 'makePDFObject'}, 'Font': {'aggiungi_oggetti': 'addObjects'}, 'TypeFace': {'ottieni_carattere_file': 'getFontFiles'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
