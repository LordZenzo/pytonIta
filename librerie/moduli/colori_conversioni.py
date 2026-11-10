"""Modulo italiano per `colorsys` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import colorsys as _orig
from colorsys import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

rgb_in_hsv = _ott(_orig, 'rgb_to_hsv')
hsv_in_rgb = _ott(_orig, 'hsv_to_rgb')
rgb_in_hls = _ott(_orig, 'rgb_to_hls')
hls_in_rgb = _ott(_orig, 'hls_to_rgb')
rgb_in_yiq = _ott(_orig, 'rgb_to_yiq')
yiq_in_rgb = _ott(_orig, 'yiq_to_rgb')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
