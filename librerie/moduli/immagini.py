"""Modulo italiano per `PIL.Image` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import PIL.Image as _orig
from PIL.Image import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

apri = _ott(_orig, 'open')
nuova = _ott(_orig, 'new')
Immagine = _ott(_orig, 'Image')
da_matrice = _ott(_orig, 'fromarray')
alias_tipo(_ott(_orig, 'Image'), {'ridimensiona': 'resize', 'ritaglia': 'crop', 'ruota': 'rotate', 'salva': 'save', 'converti': 'convert', 'miniatura': 'thumbnail', 'copia': 'copy', 'mostra': 'show', 'ottieni_pixel': 'getpixel', 'metti_pixel': 'putpixel', 'incolla': 'paste', 'dimensione': 'size', 'formato': 'format', 'modo': 'mode', 'larghezza': 'width', 'altezza': 'height', 'trasponi': 'transpose', 'dividi_canali': 'split', 'filtra': 'filter'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'RIQUADRO': 'BOX', 'ESTENSIONE': 'EXTENSION', 'CAPOVOLGI_SINISTRA_DESTRA': 'FLIP_LEFT_RIGHT', 'CAPOVOLGI_ALTO_BASSO': 'FLIP_TOP_BOTTOM', 'IMMAGINE_MASSIMO_PIXEL': 'MAX_IMAGE_PIXELS', 'PIU_VICINO': 'NEAREST', 'NESSUNO': 'NONE', 'APRI': 'OPEN', 'ORDINATO': 'ORDERED', 'INTEGRA_QUADRATURA': 'QUAD', 'RUOTA_180': 'ROTATE_180', 'RUOTA_270': 'ROTATE_270', 'RUOTA_90': 'ROTATE_90', 'SALVA': 'SAVE', 'SALVA_TUTTI': 'SAVE_ALL', 'TRASPONI': 'TRANSPOSE', 'annotazioni': 'annotations', 'fondi': 'blend', 'valuta': 'eval', 'da_byte': 'frombytes', 'inizializza': 'init', 'è_percorso': 'is_path', 'elemento': 'item', 'lineare_gradiente': 'linear_gradient', 'unisci': 'merge', 'registra_estensione': 'register_extension', 'registra_estensioni': 'register_extensions', 'registra_apri': 'register_open', 'registra_salva': 'register_save', 'registra_salva_tutti': 'register_save_all'}
_AUTO_TIPI = {'Dither': {'NESSUNO': 'NONE', 'ORDINATO': 'ORDERED'}, 'Exif': {'carica': 'load', 'in_byte': 'tobytes'}, 'Image': {'applica_trasparenza': 'apply_transparency', 'chiudi': 'close', 'converti': 'convert', 'copia': 'copy', 'ritaglia': 'crop', 'entropia': 'entropy', 'filtra': 'filter', 'formatta': 'format', 'formatta_descrizione': 'format_description', 'da_byte': 'frombytes', 'ha_trasparenza_dati': 'has_transparency_data', 'altezza': 'height', 'istogramma': 'histogram', 'carica': 'load', 'modalita': 'mode', 'incolla': 'paste', 'punto': 'point', 'quantizza': 'quantize', 'sola_lettura': 'readonly', 'riduci': 'reduce', 'ridimensiona': 'resize', 'ruota': 'rotate', 'salva': 'save', 'posiziona': 'seek', 'mostra': 'show', 'dimensione': 'size', 'separa': 'split', 'posizione': 'tell', 'in_byte': 'tobytes', 'trasformazione': 'transform', 'trasponi': 'transpose', 'verifica': 'verify', 'larghezza': 'width'}, 'ImagePointHandler': {'punto': 'point'}, 'ImageTransformHandler': {'trasformazione': 'transform'}, 'Resampling': {'RIQUADRO': 'BOX', 'PIU_VICINO': 'NEAREST'}, 'Transform': {'ESTENSIONE': 'EXTENT', 'INTEGRA_QUADRATURA': 'QUAD'}, 'Transpose': {'CAPOVOLGI_SINISTRA_DESTRA': 'FLIP_LEFT_RIGHT', 'CAPOVOLGI_ALTO_BASSO': 'FLIP_TOP_BOTTOM', 'RUOTA_180': 'ROTATE_180', 'RUOTA_270': 'ROTATE_270', 'RUOTA_90': 'ROTATE_90', 'TRASPONI': 'TRANSPOSE'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
