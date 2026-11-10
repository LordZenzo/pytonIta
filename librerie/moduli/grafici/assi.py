"""Modulo italiano per `matplotlib.axes` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import matplotlib.axes as _orig
from matplotlib.axes import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

_OPZ = {'etichetta': 'label', 'colore': 'color', 'spessore_linea': 'linewidth', 'stile_linea': 'linestyle', 'marcatore': 'marker', 'trasparenza': 'alpha', 'dimensione_figura': 'figsize', 'risoluzione': 'dpi', 'intervalli': 'bins', 'dimensione_carattere': 'fontsize', 'posizione': 'loc', 'dimensione': 's', 'colore_punti': 'c', 'mappa_colori': 'cmap', 'colore_bordo': 'edgecolor', 'colori': 'colors', 'larghezza': 'width', 'altezza': 'height', 'righe': 'nrows', 'colonne': 'ncols', 'condividi_x': 'sharex', 'condividi_y': 'sharey', 'riempimento': 'fill'}
_VAL = {}
kw_tipo(_ott(_orig, 'Axes'), ['plot', 'scatter', 'bar', 'barh', 'hist', 'text', 'annotate', 'legend', 'fill_between', 'errorbar', 'imshow', 'pie', 'set_title', 'set_xlabel', 'set_ylabel', 'grid', 'axhline', 'axvline', 'boxplot'], _OPZ, _VAL)
alias_tipo(_ott(_orig, 'Axes'), {'traccia': 'plot', 'imposta_titolo': 'set_title', 'imposta_etichetta_x': 'set_xlabel', 'imposta_etichetta_y': 'set_ylabel', 'legenda': 'legend', 'griglia': 'grid', 'barre': 'bar', 'barre_orizzontali': 'barh', 'istogramma': 'hist', 'dispersione': 'scatter', 'imposta_limiti_x': 'set_xlim', 'imposta_limiti_y': 'set_ylim', 'testo': 'text', 'annota': 'annotate', 'mostra_immagine': 'imshow', 'torta': 'pie', 'riempi_tra': 'fill_between', 'barre_errore': 'errorbar', 'linea_orizzontale': 'axhline', 'linea_verticale': 'axvline', 'scatola_baffi': 'boxplot', 'imposta_tacche_x': 'set_xticks', 'imposta_tacche_y': 'set_yticks', 'imposta_scala_x': 'set_xscale', 'imposta_scala_y': 'set_yscale', 'cancella': 'clear', 'ottieni_limiti_x': 'get_xlim', 'ottieni_limiti_y': 'get_ylim', 'disattiva_assi': 'set_axis_off'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'sottografico_classe_fabbrica': 'subplot_class_factory'}
_AUTO_TIPI = {'Axes': {'angolo_spettro': 'angle_spectrum', 'freccia': 'arrow', 'barre': 'bar', 'barre_etichetta': 'bar_label', 'barre_orizzontali': 'barh', 'scatola_baffi': 'boxplot', 'rotto_barre_orizzontali': 'broken_barh', 'contorno': 'contour', 'contorno_pieno': 'contourf', 'riempi': 'fill', 'riempi_tra': 'fill_between', 'ottieni_titolo': 'get_title', 'raggruppato_barre': 'grouped_bar', 'esagoni': 'hexbin', 'istogramma': 'hist', 'linee_orizzontali': 'hlines', 'mostra_immagine': 'imshow', 'indica_incasso': 'indicate_inset', 'indica_incasso_ingrandisci': 'indicate_inset_zoom', 'incasso_assi': 'inset_axes', 'legenda': 'legend', 'log_log': 'loglog', 'ampiezza_spettro': 'magnitude_spectrum', 'torta': 'pie', 'torta_etichetta': 'pie_label', 'traccia': 'plot', 'campo_vettoriale': 'quiver', 'dispersione': 'scatter', 'secondario_asse_x': 'secondary_xaxis', 'secondario_asse_y': 'secondary_yaxis', 'semilog_x': 'semilogx', 'semilog_y': 'semilogy', 'imposta': 'set', 'imposta_titolo': 'set_title', 'struttura': 'spy', 'grafico_impilato': 'stackplot', 'gradini': 'stairs', 'nome_senza_estensione': 'stem', 'passo': 'step', 'tabella': 'table', 'testo': 'text', 'grafico_violino': 'violinplot', 'linee_verticali': 'vlines'}, 'Subplot': {'angolo_spettro': 'angle_spectrum', 'freccia': 'arrow', 'barre': 'bar', 'barre_etichetta': 'bar_label', 'barre_orizzontali': 'barh', 'scatola_baffi': 'boxplot', 'rotto_barre_orizzontali': 'broken_barh', 'contorno': 'contour', 'contorno_pieno': 'contourf', 'riempi': 'fill', 'riempi_tra': 'fill_between', 'ottieni_titolo': 'get_title', 'raggruppato_barre': 'grouped_bar', 'esagoni': 'hexbin', 'istogramma': 'hist', 'linee_orizzontali': 'hlines', 'mostra_immagine': 'imshow', 'indica_incasso': 'indicate_inset', 'indica_incasso_ingrandisci': 'indicate_inset_zoom', 'incasso_assi': 'inset_axes', 'legenda': 'legend', 'log_log': 'loglog', 'ampiezza_spettro': 'magnitude_spectrum', 'torta': 'pie', 'torta_etichetta': 'pie_label', 'traccia': 'plot', 'campo_vettoriale': 'quiver', 'dispersione': 'scatter', 'secondario_asse_x': 'secondary_xaxis', 'secondario_asse_y': 'secondary_yaxis', 'semilog_x': 'semilogx', 'semilog_y': 'semilogy', 'imposta': 'set', 'imposta_titolo': 'set_title', 'struttura': 'spy', 'grafico_impilato': 'stackplot', 'gradini': 'stairs', 'nome_senza_estensione': 'stem', 'passo': 'step', 'tabella': 'table', 'testo': 'text', 'grafico_violino': 'violinplot', 'linee_verticali': 'vlines'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
