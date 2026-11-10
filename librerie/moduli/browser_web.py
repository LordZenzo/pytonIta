"""Modulo italiano per `webbrowser` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import webbrowser as _orig
from webbrowser import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

apri = _ott(_orig, 'open')
apri_nuova_scheda = _ott(_orig, 'open_new_tab')
apri_nuova_finestra = _ott(_orig, 'open_new')
ottieni = _ott(_orig, 'get')
registra = _ott(_orig, 'register')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'BaseBrowser': {'argomenti': 'args'}, 'Chrome': {'sfondo': 'background', 'remoto_azione': 'remote_action', 'remoto_azione_nuova_scheda': 'remote_action_newtab', 'remoto_azione_nuova_finestra': 'remote_action_newwin', 'remoto_argomenti': 'remote_args'}, 'Chromium': {'sfondo': 'background', 'remoto_azione': 'remote_action', 'remoto_azione_nuova_scheda': 'remote_action_newtab', 'remoto_azione_nuova_finestra': 'remote_action_newwin', 'remoto_argomenti': 'remote_args'}, 'Edge': {'sfondo': 'background', 'remoto_azione': 'remote_action', 'remoto_azione_nuova_scheda': 'remote_action_newtab', 'remoto_azione_nuova_finestra': 'remote_action_newwin', 'remoto_argomenti': 'remote_args'}, 'Elinks': {'sfondo': 'background', 'reindirizza_uscita_standard': 'redirect_stdout', 'remoto_azione': 'remote_action', 'remoto_azione_nuova_scheda': 'remote_action_newtab', 'remoto_azione_nuova_finestra': 'remote_action_newwin', 'remoto_argomenti': 'remote_args'}, 'Epiphany': {'sfondo': 'background', 'remoto_azione': 'remote_action', 'remoto_azione_nuova_finestra': 'remote_action_newwin', 'remoto_argomenti': 'remote_args'}, 'Mozilla': {'sfondo': 'background', 'remoto_azione': 'remote_action', 'remoto_azione_nuova_scheda': 'remote_action_newtab', 'remoto_azione_nuova_finestra': 'remote_action_newwin', 'remoto_argomenti': 'remote_args'}, 'Opera': {'sfondo': 'background', 'remoto_azione': 'remote_action', 'remoto_azione_nuova_scheda': 'remote_action_newtab', 'remoto_azione_nuova_finestra': 'remote_action_newwin', 'remoto_argomenti': 'remote_args'}, 'UnixBrowser': {'sfondo': 'background', 'reindirizza_uscita_standard': 'redirect_stdout', 'remoto_azione': 'remote_action', 'remoto_azione_nuova_scheda': 'remote_action_newtab', 'remoto_azione_nuova_finestra': 'remote_action_newwin', 'remoto_argomenti': 'remote_args'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
