"""Modulo italiano per `tkinter.messagebox` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import tkinter.messagebox as _orig
from tkinter.messagebox import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

mostra_info = _ott(_orig, 'showinfo')
mostra_avviso = _ott(_orig, 'showwarning')
mostra_errore = _ott(_orig, 'showerror')
chiedi_domanda = _ott(_orig, 'askquestion')
chiedi_ok_annulla = _ott(_orig, 'askokcancel')
chiedi_si_no = _ott(_orig, 'askyesno')
chiedi_si_no_annulla = _ott(_orig, 'askyesnocancel')
chiedi_riprova_annulla = _ott(_orig, 'askretrycancel')
_OPZ = {'titolo': 'title', 'messaggio': 'message', 'genitore': 'parent', 'icona': 'icon', 'dettaglio': 'detail', 'predefinito': 'default'}
_VAL = {}

from _italiano import traduci_kw as _tr
_O = {'titolo': 'title', 'messaggio': 'message', 'genitore': 'parent',
      'icona': 'icon', 'dettaglio': 'detail', 'predefinito': 'default'}
for _n in ('mostra_info', 'mostra_avviso', 'mostra_errore', 'chiedi_domanda',
           'chiedi_ok_annulla', 'chiedi_si_no', 'chiedi_si_no_annulla',
           'chiedi_riprova_annulla'):
    globals()[_n] = _tr(globals()[_n], _O)

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'Dialog': {'comando': 'command', 'mostra': 'show'}, 'Message': {'comando': 'command'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
