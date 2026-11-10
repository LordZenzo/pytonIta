"""Modulo italiano per `tkinter.scrolledtext` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import tkinter.scrolledtext as _orig
from tkinter.scrolledtext import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

TestoScorrevole = _ott(_orig, 'ScrolledText')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'Grid': {'rettangolo_contenitore': 'bbox', 'configura_colonna': 'columnconfigure', 'configura': 'config', 'dimentica': 'forget', 'griglia': 'grid', 'griglia_rettangolo_contenitore': 'grid_bbox', 'griglia_configura_colonna': 'grid_columnconfigure', 'griglia_configura': 'grid_configure', 'griglia_dimentica': 'grid_forget', 'griglia_informazione': 'grid_info', 'griglia_posizione': 'grid_location', 'griglia_propaga': 'grid_propagate', 'griglia_rimuovi': 'grid_remove', 'griglia_configura_riga': 'grid_rowconfigure', 'griglia_dimensione': 'grid_size', 'griglia_elementi': 'grid_slaves', 'informazioni': 'info', 'posizione': 'location', 'propaga': 'propagate', 'configura_riga': 'rowconfigure', 'dimensione': 'size', 'elementi': 'slaves'}, 'Pack': {'configura': 'config', 'dimentica': 'forget', 'informazioni': 'info', 'impacchetta': 'pack', 'impacchetta_configura': 'pack_configure', 'impacchetta_dimentica': 'pack_forget', 'impacchetta_informazione': 'pack_info', 'impacchetta_propaga': 'pack_propagate', 'impacchetta_elementi': 'pack_slaves', 'propaga': 'propagate', 'elementi': 'slaves'}, 'Place': {'configura': 'config', 'dimentica': 'forget', 'informazioni': 'info', 'posiziona': 'place', 'posiziona_configura': 'place_configure', 'posiziona_dimentica': 'place_forget', 'posiziona_informazione': 'place_info', 'posiziona_elementi': 'place_slaves', 'elementi': 'slaves'}, 'Scrollbar': {'attiva': 'activate', 'frazione': 'fraction', 'ottieni': 'get', 'identifica': 'identify', 'imposta': 'set'}, 'Text': {'rettangolo_contenitore': 'bbox', 'confronta': 'compare', 'conta': 'count', 'cancella': 'delete', 'scarica': 'dump', 'modifica': 'edit', 'modifica_modificato': 'edit_modified', 'modifica_ripeti': 'edit_redo', 'modifica_reimposta': 'edit_reset', 'modifica_separatore': 'edit_separator', 'modifica_annulla': 'edit_undo', 'ottieni': 'get', 'immagine_ottieni_opzione': 'image_cget', 'immagine_configura': 'image_configure', 'immagine_crea': 'image_create', 'immagine_nomi': 'image_names', 'indice': 'index', 'inserisci': 'insert', 'segna_nomi': 'mark_names', 'segna_successivo': 'mark_next', 'segna_precedente': 'mark_previous', 'segna_insieme': 'mark_set', 'pari_crea': 'peer_create', 'pari_nomi': 'peer_names', 'sostituisci': 'replace', 'scansiona_segna': 'scan_mark', 'cerca': 'search', 'mostra': 'see', 'tag_aggiungi': 'tag_add', 'tag_associa': 'tag_bind', 'tag_ottieni_opzione': 'tag_cget', 'configura_tag': 'tag_config', 'tag_configura': 'tag_configure', 'tag_cancella': 'tag_delete', 'tag_minuscolo': 'tag_lower', 'tag_nomi': 'tag_names', 'tag_solleva': 'tag_raise', 'tag_intervalli': 'tag_ranges', 'tag_rimuovi': 'tag_remove', 'tag_dissocia': 'tag_unbind', 'finestra_ottieni_opzione': 'window_cget', 'finestra_configurazione': 'window_config', 'finestra_configura': 'window_configure', 'finestra_crea': 'window_create', 'finestra_nomi': 'window_names'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
