"""Modulo italiano per `reportlab.lib.styles` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import reportlab.lib.styles as _orig
from reportlab.lib.styles import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

ottieni_stili_esempio = _ott(_orig, 'getSampleStyleSheet')
StileParagrafo = _ott(_orig, 'ParagraphStyle')
_OPZ = {'nome': 'name', 'genitore': 'parent', 'nome_carattere': 'fontName', 'dimensione_carattere': 'fontSize', 'interlinea': 'leading', 'allineamento': 'alignment', 'colore_testo': 'textColor', 'spazio_dopo': 'spaceAfter', 'spazio_prima': 'spaceBefore', 'rientro_sinistro': 'leftIndent', 'rientro_destro': 'rightIndent'}
_VAL = {}
kw_tipo(_ott(_orig, 'ParagraphStyle'), ['__init__'], _OPZ, _VAL)

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'LineStyle': {'predefiniti': 'defaults', 'prepara_tela': 'prepareCanvas'}, 'ListStyle': {'predefiniti': 'defaults'}, 'ParagraphStyle': {'predefiniti': 'defaults'}, 'PropertySet': {'clona': 'clone', 'predefiniti': 'defaults', 'elenca_attributi': 'listAttrs'}, 'StyleSheet1': {'aggiungi': 'add', 'ottieni': 'get', 'ha_chiave': 'has_key', 'elenca': 'list'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
