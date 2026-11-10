"""Modulo italiano per `turtle` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import turtle as _orig
from turtle import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

Tartaruga = _ott(_orig, 'Turtle')
Schermo = _ott(_orig, 'Screen')
TartarugaGrezza = _ott(_orig, 'RawTurtle')
avanti = _ott(_orig, 'forward')
indietro = _ott(_orig, 'backward')
sinistra = _ott(_orig, 'left')
destra = _ott(_orig, 'right')
alza_penna = _ott(_orig, 'penup')
abbassa_penna = _ott(_orig, 'pendown')
vai_a = _ott(_orig, 'goto')
colore = _ott(_orig, 'color')
colore_penna = _ott(_orig, 'pencolor')
colore_riempimento = _ott(_orig, 'fillcolor')
inizia_riempimento = _ott(_orig, 'begin_fill')
termina_riempimento = _ott(_orig, 'end_fill')
cerchio = _ott(_orig, 'circle')
velocita = _ott(_orig, 'speed')
ciclo_principale = _ott(_orig, 'mainloop')
spessore_penna = _ott(_orig, 'pensize')
nascondi_tartaruga = _ott(_orig, 'hideturtle')
mostra_tartaruga = _ott(_orig, 'showturtle')
cancella = _ott(_orig, 'clear')
reimposta = _ott(_orig, 'reset')
scrivi = _ott(_orig, 'write')
imposta_posizione = _ott(_orig, 'setpos')
imposta_direzione = _ott(_orig, 'setheading')
punto = _ott(_orig, 'dot')
timbro = _ott(_orig, 'stamp')
esci_al_clic = _ott(_orig, 'exitonclick')
imposta_sfondo = _ott(_orig, 'bgcolor')
titolo = _ott(_orig, 'title')
ascolta = _ott(_orig, 'listen')
al_tasto = _ott(_orig, 'onkey')
al_clic = _ott(_orig, 'onscreenclick')
dopo = _ott(_orig, 'ontimer')
posizione = _ott(_orig, 'position')
direzione = _ott(_orig, 'heading')
distanza = _ott(_orig, 'distance')
alias_tipo(_ott(_orig, 'RawTurtle'), {'avanti': 'forward', 'indietro': 'backward', 'sinistra': 'left', 'destra': 'right', 'alza_penna': 'penup', 'abbassa_penna': 'pendown', 'vai_a': 'goto', 'colore': 'color', 'cerchio': 'circle', 'velocita': 'speed'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'clona': 'clone', 'ritardo': 'delay', 'giu': 'down', 'casa': 'home', 'modalita': 'mode', 'registra_forma': 'register_shape', 'forma': 'shape', 'annulla': 'undo', 'su': 'up', 'aggiorna': 'update', 'larghezza': 'width', 'finestra_altezza': 'window_height', 'finestra_larghezza': 'window_width'}
_AUTO_TIPI = {'RawPen': {'clona': 'clone', 'forma': 'shape', 'annulla': 'undo'}, 'RawTurtle': {'clona': 'clone', 'forma': 'shape', 'annulla': 'undo'}, 'ScrolledCanvas': {'aggiungi_tag': 'addtag', 'aggiungi_tag_sopra': 'addtag_above', 'aggiungi_tag_tutti': 'addtag_all', 'aggiungi_tag_sotto': 'addtag_below', 'aggiungi_tag_piu_vicino': 'addtag_closest', 'aggiungi_tag_racchiuso': 'addtag_enclosed', 'aggiungi_tag_sovrapposti': 'addtag_overlapping', 'aggiungi_tag_con_tag': 'addtag_withtag', 'rettangolo_contenitore': 'bbox', 'associa': 'bind', 'ottieni_opzione': 'cget', 'configura': 'config', 'coordinate': 'coords', 'crea_arco': 'create_arc', 'crea_bitmap': 'create_bitmap', 'crea_immagine': 'create_image', 'crea_linea': 'create_line', 'crea_testo': 'create_text', 'crea_finestra': 'create_window', 'cancella': 'delete', 'trova': 'find', 'trova_sopra': 'find_above', 'trova_tutti': 'find_all', 'trova_sotto': 'find_below', 'trova_piu_vicino': 'find_closest', 'trova_racchiuso': 'find_enclosed', 'trova_sovrapposti': 'find_overlapping', 'trova_con_tag': 'find_withtag', 'focus_forza': 'focus_force', 'posizione_cursore': 'icursor', 'indice': 'index', 'inserisci': 'insert', 'ottieni_opzione_elemento': 'itemcget', 'configura_elemento': 'itemconfig', 'sposta': 'move', 'sposta_a': 'moveto', 'su_ridimensiona': 'onResize', 'scala': 'scale', 'scansiona_segna': 'scan_mark', 'seleziona_regola': 'select_adjust', 'seleziona_svuota': 'select_clear', 'seleziona_da': 'select_from', 'seleziona_elemento': 'select_item', 'seleziona_fino_a': 'select_to', 'tag_associa': 'tag_bind', 'tag_minuscolo': 'tag_lower', 'tag_solleva': 'tag_raise', 'tag_dissocia': 'tag_unbind', 'tipo': 'type', 'dissocia': 'unbind', 'scorri_x': 'xview', 'scorri_x_sposta_a': 'xview_moveto', 'scorri_x_scorri': 'xview_scroll', 'scorri_y': 'yview', 'scorri_y_sposta_a': 'yview_moveto', 'scorri_y_scorri': 'yview_scroll'}, 'TNavigator': {'MODALITA_PREDEFINITO': 'DEFAULT_MODE', 'indietro': 'back', 'casa': 'home', 'posizione': 'pos'}, 'TPen': {'giu': 'down', 'su': 'up', 'larghezza': 'width'}, 'Tbuffer': {'estrai': 'pop', 'inserisci': 'push'}, 'TurtleScreen': {'ritardo': 'delay', 'modalita': 'mode', 'registra_forma': 'register_shape', 'aggiorna': 'update', 'finestra_altezza': 'window_height', 'finestra_larghezza': 'window_width'}, 'Vec2D': {'ruota': 'rotate'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
