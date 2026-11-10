"""Modulo italiano per `math` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import math as _orig
from math import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

radice_quadrata = _ott(_orig, 'sqrt')
pigreco = _ott(_orig, 'pi')
numero_di_nepero = _ott(_orig, 'e')
tau = _ott(_orig, 'tau')
pavimento = _ott(_orig, 'floor')
soffitto = _ott(_orig, 'ceil')
seno = _ott(_orig, 'sin')
coseno = _ott(_orig, 'cos')
tangente = _ott(_orig, 'tan')
arcoseno = _ott(_orig, 'asin')
arcocoseno = _ott(_orig, 'acos')
arcotangente = _ott(_orig, 'atan')
arcotangente2 = _ott(_orig, 'atan2')
seno_iperbolico = _ott(_orig, 'sinh')
coseno_iperbolico = _ott(_orig, 'cosh')
tangente_iperbolica = _ott(_orig, 'tanh')
logaritmo = _ott(_orig, 'log')
logaritmo_10 = _ott(_orig, 'log10')
logaritmo_2 = _ott(_orig, 'log2')
logaritmo_1_piu = _ott(_orig, 'log1p')
esponenziale = _ott(_orig, 'exp')
esponenziale_meno_1 = _ott(_orig, 'expm1')
fattoriale = _ott(_orig, 'factorial')
mcd = _ott(_orig, 'gcd')
mcm = _ott(_orig, 'lcm')
infinito = _ott(_orig, 'inf')
gradi = _ott(_orig, 'degrees')
radianti = _ott(_orig, 'radians')
valore_assoluto = _ott(_orig, 'fabs')
tronca = _ott(_orig, 'trunc')
ipotenusa = _ott(_orig, 'hypot')
distanza = _ott(_orig, 'dist')
potenza_decimale = _ott(_orig, 'pow')
combinazioni = _ott(_orig, 'comb')
permutazioni = _ott(_orig, 'perm')
è_nan = _ott(_orig, 'isnan')
è_infinito = _ott(_orig, 'isinf')
è_finito = _ott(_orig, 'isfinite')
è_vicino = _ott(_orig, 'isclose')
somma_esatta = _ott(_orig, 'fsum')
prodotto = _ott(_orig, 'prod')
radice_intera = _ott(_orig, 'isqrt')
resto = _ott(_orig, 'fmod')
copia_segno = _ott(_orig, 'copysign')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'non_numero': 'nan'}
_AUTO_TIPI = {}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
