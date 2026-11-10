"""Modulo italiano per `statistics` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import statistics as _orig
from statistics import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

media = _ott(_orig, 'mean')
media_decimale = _ott(_orig, 'fmean')
media_geometrica = _ott(_orig, 'geometric_mean')
media_armonica = _ott(_orig, 'harmonic_mean')
mediana = _ott(_orig, 'median')
mediana_bassa = _ott(_orig, 'median_low')
mediana_alta = _ott(_orig, 'median_high')
moda = _ott(_orig, 'mode')
mode_multiple = _ott(_orig, 'multimode')
deviazione_standard_popolazione = _ott(_orig, 'pstdev')
deviazione_standard = _ott(_orig, 'stdev')
varianza_popolazione = _ott(_orig, 'pvariance')
varianza = _ott(_orig, 'variance')
quantili = _ott(_orig, 'quantiles')
correlazione = _ott(_orig, 'correlation')
covarianza = _ott(_orig, 'covariance')
regressione_lineare = _ott(_orig, 'linear_regression')
DistribuzioneNormale = _ott(_orig, 'NormalDist')
ErroreStatistica = _ott(_orig, 'StatisticsError')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'mediana_raggruppato': 'median_grouped'}
_AUTO_TIPI = {}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
