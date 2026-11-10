"""Modulo italiano per `tkinter.filedialog` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import tkinter.filedialog as _orig
from tkinter.filedialog import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

chiedi_file_da_aprire = _ott(_orig, 'askopenfilename')
chiedi_file_da_salvare = _ott(_orig, 'asksaveasfilename')
chiedi_cartella = _ott(_orig, 'askdirectory')
chiedi_file_multipli = _ott(_orig, 'askopenfilenames')
apri_file = _ott(_orig, 'askopenfile')
salva_file = _ott(_orig, 'asksaveasfile')

from _italiano import traduci_kw as _tr
_O = {'titolo': 'title', 'cartella_iniziale': 'initialdir',
      'tipi_file': 'filetypes', 'estensione_predefinita': 'defaultextension',
      'file_iniziale': 'initialfile', 'genitore': 'parent', 'modo': 'mode'}
for _n in ('chiedi_file_da_aprire', 'chiedi_file_da_salvare', 'chiedi_cartella',
           'chiedi_file_multipli', 'apri_file', 'salva_file'):
    globals()[_n] = _tr(globals()[_n], _O)

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'Button': {'lampeggia': 'flash', 'invoca': 'invoke'}, 'Dialog': {'distruggi': 'destroy'}, 'Directory': {'comando': 'command'}, 'Entry': {'cancella': 'delete', 'ottieni': 'get', 'posizione_cursore': 'icursor', 'indice': 'index', 'inserisci': 'insert', 'scansiona_segna': 'scan_mark', 'seleziona_regola': 'select_adjust', 'seleziona_svuota': 'select_clear', 'seleziona_da': 'select_from', 'seleziona_presente': 'select_present', 'seleziona_intervallo': 'select_range', 'seleziona_fino_a': 'select_to', 'selezione_regola': 'selection_adjust', 'selezione_svuota': 'selection_clear', 'selezione_da': 'selection_from', 'selezione_presente': 'selection_present', 'selezione_intervallo': 'selection_range', 'selezione_fino_a': 'selection_to'}, 'FileDialog': {'annulla_comando': 'cancel_command', 'file_evento_doppio': 'files_double_event', 'file_seleziona_evento': 'files_select_event', 'filtra_comando': 'filter_command', 'ottieni_filtra': 'get_filter', 'ottieni_selezione': 'get_selection', 'ok_comando': 'ok_command', 'ok_evento': 'ok_event', 'esci': 'quit', 'imposta_filtra': 'set_filter', 'imposta_selezione': 'set_selection', 'titolo': 'title'}, 'Listbox': {'attiva': 'activate', 'rettangolo_contenitore': 'bbox', 'selezione_corrente': 'curselection', 'cancella': 'delete', 'ottieni': 'get', 'indice': 'index', 'inserisci': 'insert', 'ottieni_opzione_elemento': 'itemcget', 'configura_elemento': 'itemconfig', 'piu_vicino': 'nearest', 'scansiona_segna': 'scan_mark', 'mostra': 'see', 'seleziona_ancora': 'select_anchor', 'seleziona_svuota': 'select_clear', 'seleziona_include': 'select_includes', 'seleziona_insieme': 'select_set', 'selezione_ancora': 'selection_anchor', 'selezione_svuota': 'selection_clear', 'selezione_include': 'selection_includes', 'selezione_insieme': 'selection_set', 'dimensione': 'size'}, 'LoadFileDialog': {'ok_comando': 'ok_command', 'titolo': 'title'}, 'Open': {'comando': 'command'}, 'SaveAs': {'comando': 'command'}, 'SaveFileDialog': {'ok_comando': 'ok_command', 'titolo': 'title'}, 'Scrollbar': {'attiva': 'activate', 'frazione': 'fraction', 'ottieni': 'get', 'identifica': 'identify', 'imposta': 'set'}, 'Tk': {'distruggi': 'destroy', 'rapporto_richiamo_eccezione': 'report_callback_exception'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
