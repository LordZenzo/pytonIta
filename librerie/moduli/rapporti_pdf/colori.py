"""Modulo italiano per `reportlab.lib.colors` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import reportlab.lib.colors as _orig
from reportlab.lib.colors import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

Colore = _ott(_orig, 'Color')
ColoreEsadecimale = _ott(_orig, 'HexColor')
nero = _ott(_orig, 'black')
bianco = _ott(_orig, 'white')
rosso = _ott(_orig, 'red')
verde = _ott(_orig, 'green')
blu = _ott(_orig, 'blue')
grigio = _ott(_orig, 'grey')
giallo = _ott(_orig, 'yellow')
arancione = _ott(_orig, 'orange')
viola = _ott(_orig, 'purple')
rosa = _ott(_orig, 'pink')
marrone = _ott(_orig, 'brown')
celeste = _ott(_orig, 'lightblue')
grigio_chiaro = _ott(_orig, 'lightgrey')
grigio_scuro = _ott(_orig, 'darkgrey')
trasparente = _ott(_orig, 'transparent')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'colore_distanza': 'colorDistance', 'descrivi': 'describe', 'ottieni_tutti_con_nome_colori': 'getAllNamedColors', 'è_testo': 'isStr', 'letterale_valuta': 'literal_eval', 'imposta_colori': 'setColors', 'in_colore': 'toColor', 'in_colore_o_nessuno': 'toColorOrNone'}
_AUTO_TIPI = {'CMYKColor': {'normalizzato_trasparenza': 'normalizedAlpha'}, 'Color': {'clona': 'clone', 'intero_rgb': 'int_rgb', 'intero_rgba': 'int_rgba', 'normalizzato_trasparenza': 'normalizedAlpha'}, 'ColorType': {'clona': 'clone', 'intero_rgb': 'int_rgb', 'intero_rgba': 'int_rgba', 'normalizzato_trasparenza': 'normalizedAlpha'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
