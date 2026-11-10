"""Modulo italiano per `tkinter.ttk` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import tkinter.ttk as _orig
from tkinter.ttk import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

Pulsante = _ott(_orig, 'Button')
Etichetta = _ott(_orig, 'Label')
Riquadro = _ott(_orig, 'Frame')
CampoTesto = _ott(_orig, 'Entry')
CasellaSelezione = _ott(_orig, 'Checkbutton')
PulsanteOpzione = _ott(_orig, 'Radiobutton')
CasellaCombinata = _ott(_orig, 'Combobox')
Albero = _ott(_orig, 'Treeview')
Schede = _ott(_orig, 'Notebook')
BarraProgresso = _ott(_orig, 'Progressbar')
BarraScorrimento = _ott(_orig, 'Scrollbar')
Cursore = _ott(_orig, 'Scale')
CampoNumerico = _ott(_orig, 'Spinbox')
Separatore = _ott(_orig, 'Separator')
RiquadroEtichettato = _ott(_orig, 'LabelFrame')
PannelloDiviso = _ott(_orig, 'PanedWindow')
PulsanteMenu = _ott(_orig, 'Menubutton')
Stile = _ott(_orig, 'Style')
Elemento = _ott(_orig, 'Widget')
MenuOpzioni = _ott(_orig, 'OptionMenu')
_OPZ = {'testo': 'text', 'comando': 'command', 'larghezza': 'width', 'altezza': 'height', 'sfondo': 'background', 'primo_piano': 'foreground', 'carattere': 'font', 'margine_x': 'padx', 'margine_y': 'pady', 'lato': 'side', 'riempi': 'fill', 'espandi': 'expand', 'riga': 'row', 'colonna': 'column', 'span_colonne': 'columnspan', 'span_righe': 'rowspan', 'aggancia': 'sticky', 'ancora': 'anchor', 'stato': 'state', 'variabile_testo': 'textvariable', 'variabile': 'variable', 'immagine': 'image', 'rilievo': 'relief', 'bordo': 'borderwidth', 'orientamento': 'orient', 'comando_scorrimento_y': 'yscrollcommand', 'comando_scorrimento_x': 'xscrollcommand', 'modalita_selezione': 'selectmode', 'mostra': 'show', 'larghezza_a_capo': 'wraplength', 'allineamento': 'justify', 'valore': 'value', 'da_': 'from_', 'a': 'to', 'risoluzione': 'resolution', 'cursore': 'cursor', 'margine_interno_x': 'ipadx', 'margine_interno_y': 'ipady', 'sfondo_attivo': 'activebackground', 'primo_piano_attivo': 'activeforeground', 'primo_piano_disabilitato': 'disabledforeground', 'sfondo_selezione': 'selectbackground', 'primo_piano_selezione': 'selectforeground', 'variabile_elenco': 'listvariable', 'a_capo': 'wrap', 'annulla': 'undo', 'imbottitura': 'padding', 'stile': 'style', 'colonne': 'columns', 'valori': 'values', 'peso': 'weight', 'dimensione_minima': 'minsize', 'strappabile': 'tearoff', 'etichetta': 'label', 'acceleratore': 'accelerator', 'sottolinea': 'underline', 'valore_attivo': 'onvalue', 'valore_non_attivo': 'offvalue', 'lunghezza': 'length', 'modalita': 'mode', 'massimo': 'maximum', 'minimo': 'minimum', 'colore_cursore': 'insertbackground', 'evidenzia_spessore': 'highlightthickness', 'esporta_selezione': 'exportselection', 'genitore': 'master', 'altezza_riga': 'rowheight', 'composto': 'compound'}
_VAL = {'side': {'sinistra': 'left', 'destra': 'right', 'alto': 'top', 'basso': 'bottom'}, 'fill': {'entrambi': 'both', 'nessuno': 'none'}, 'anchor': {'nord': 'n', 'sud': 's', 'est': 'e', 'ovest': 'w', 'centro': 'center'}, 'state': {'normale': 'normal', 'disabilitato': 'disabled', 'attivo': 'active', 'sola_lettura': 'readonly'}, 'relief': {'piatto': 'flat', 'rialzato': 'raised', 'incavato': 'sunken', 'scanalato': 'groove', 'bordo': 'ridge', 'solido': 'solid'}, 'orient': {'orizzontale': 'horizontal', 'verticale': 'vertical'}, 'justify': {'sinistra': 'left', 'centro': 'center', 'destra': 'right'}, 'wrap': {'nessuno': 'none', 'carattere': 'char', 'parola': 'word'}, 'selectmode': {'singola': 'single', 'multipla': 'multiple', 'estesa': 'extended'}, 'compound': {'alto': 'top', 'basso': 'bottom', 'sinistra': 'left', 'destra': 'right', 'centro': 'center', 'nessuno': 'none'}}
kw_tipo(_ott(_orig, 'Button'), ['__init__'], _OPZ, _VAL)
kw_tipo(_ott(_orig, 'Label'), ['__init__'], _OPZ, _VAL)
kw_tipo(_ott(_orig, 'Frame'), ['__init__'], _OPZ, _VAL)
kw_tipo(_ott(_orig, 'Entry'), ['__init__'], _OPZ, _VAL)
kw_tipo(_ott(_orig, 'Checkbutton'), ['__init__'], _OPZ, _VAL)
kw_tipo(_ott(_orig, 'Radiobutton'), ['__init__'], _OPZ, _VAL)
kw_tipo(_ott(_orig, 'Combobox'), ['__init__'], _OPZ, _VAL)
kw_tipo(_ott(_orig, 'Treeview'), ['__init__'], _OPZ, _VAL)
kw_tipo(_ott(_orig, 'Notebook'), ['__init__'], _OPZ, _VAL)
kw_tipo(_ott(_orig, 'Progressbar'), ['__init__'], _OPZ, _VAL)
kw_tipo(_ott(_orig, 'Scrollbar'), ['__init__'], _OPZ, _VAL)
kw_tipo(_ott(_orig, 'Scale'), ['__init__'], _OPZ, _VAL)
kw_tipo(_ott(_orig, 'Spinbox'), ['__init__'], _OPZ, _VAL)
kw_tipo(_ott(_orig, 'Separator'), ['__init__'], _OPZ, _VAL)
kw_tipo(_ott(_orig, 'LabelFrame'), ['__init__'], _OPZ, _VAL)
kw_tipo(_ott(_orig, 'PanedWindow'), ['__init__'], _OPZ, _VAL)
kw_tipo(_ott(_orig, 'Menubutton'), ['__init__'], _OPZ, _VAL)
kw_tipo(_ott(_orig, 'Widget'), ['configure', 'config'], _OPZ, _VAL)
alias_tipo(_ott(_orig, 'Widget'), {'stato': 'state', 'in_stato': 'instate', 'identifica': 'identify'})
alias_tipo(_ott(_orig, 'Treeview'), {'intestazione': 'heading', 'colonna': 'column', 'inserisci': 'insert', 'cancella': 'delete', 'ottieni_figli': 'get_children', 'elemento': 'item', 'selezione': 'selection', 'imposta': 'set', 'sposta': 'move', 'mostra': 'see', 'identifica_riga': 'identify_row', 'identifica_colonna': 'identify_column', 'genitore': 'parent', 'esiste': 'exists', 'configura_tag': 'tag_configure', 'stacca': 'detach', 'successivo': 'next', 'precedente': 'prev', 'indice': 'index', 'rettangolo_contenitore': 'bbox', 'ricollega': 'reattach', 'seleziona': 'selection_set', 'aggiungi_selezione': 'selection_add', 'rimuovi_selezione': 'selection_remove'})
alias_tipo(_ott(_orig, 'Combobox'), {'corrente': 'current', 'imposta': 'set', 'ottieni': 'get'})
alias_tipo(_ott(_orig, 'Notebook'), {'aggiungi': 'add', 'scheda': 'tab', 'seleziona': 'select', 'schede': 'tabs', 'indice': 'index', 'dimentica': 'forget', 'nascondi': 'hide', 'inserisci': 'insert'})
alias_tipo(_ott(_orig, 'Progressbar'), {'avvia': 'start', 'ferma': 'stop', 'passo': 'step'})
alias_tipo(_ott(_orig, 'Style'), {'configura': 'configure', 'mappa': 'map', 'usa_tema': 'theme_use', 'nomi_temi': 'theme_names', 'cerca': 'lookup', 'disposizione': 'layout', 'crea_tema': 'theme_create'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'Button': {'invoca': 'invoke'}, 'Checkbutton': {'invoca': 'invoke'}, 'Combobox': {'corrente': 'current', 'imposta': 'set'}, 'Entry': {'rettangolo_contenitore': 'bbox', 'identifica': 'identify', 'convalida': 'validate'}, 'LabeledScale': {'distruggi': 'destroy', 'valore': 'value'}, 'Notebook': {'aggiungi': 'add', 'dimentica': 'forget', 'nascondi': 'hide', 'identifica': 'identify', 'indice': 'index', 'inserisci': 'insert', 'seleziona': 'select', 'scheda': 'tab', 'schede': 'tabs'}, 'OptionMenu': {'distruggi': 'destroy', 'imposta_menu': 'set_menu'}, 'PanedWindow': {'dimentica': 'forget', 'inserisci': 'insert'}, 'Panedwindow': {'dimentica': 'forget', 'inserisci': 'insert'}, 'Progressbar': {'avvia': 'start', 'passo': 'step', 'ferma': 'stop'}, 'Radiobutton': {'invoca': 'invoke'}, 'Scale': {'configura': 'configure', 'ottieni': 'get'}, 'Spinbox': {'imposta': 'set'}, 'Style': {'configura': 'configure', 'elemento_crea': 'element_create', 'elemento_nomi': 'element_names', 'elemento_opzioni': 'element_options', 'disposizione': 'layout', 'mappa': 'map', 'tema_crea': 'theme_create', 'tema_nomi': 'theme_names', 'tema_impostazioni': 'theme_settings', 'tema_usa': 'theme_use'}, 'Treeview': {'rettangolo_contenitore': 'bbox', 'colonna': 'column', 'cancella': 'delete', 'stacca': 'detach', 'esiste': 'exists', 'ottieni_figli': 'get_children', 'identifica': 'identify', 'identifica_colonna': 'identify_column', 'identifica_elemento': 'identify_element', 'identifica_riga': 'identify_row', 'indice': 'index', 'inserisci': 'insert', 'elemento': 'item', 'sposta': 'move', 'successivo': 'next', 'genitore': 'parent', 'precedente': 'prev', 'mostra': 'see', 'selezione': 'selection', 'selezione_aggiungi': 'selection_add', 'selezione_rimuovi': 'selection_remove', 'selezione_insieme': 'selection_set', 'selezione_inverti': 'selection_toggle', 'imposta': 'set', 'imposta_figli': 'set_children', 'tag_associa': 'tag_bind', 'tag_configura': 'tag_configure', 'tag_ha': 'tag_has'}, 'Widget': {'identifica': 'identify', 'stato': 'state'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
