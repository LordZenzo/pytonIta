"""Modulo italiano per `decimal` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import decimal as _orig
from decimal import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

Decimale = _ott(_orig, 'Decimal')
ottieni_contesto = _ott(_orig, 'getcontext')
imposta_contesto = _ott(_orig, 'setcontext')
contesto_locale = _ott(_orig, 'localcontext')
Contesto = _ott(_orig, 'Context')
ARROTONDA_MEZZO_SU = _ott(_orig, 'ROUND_HALF_UP')
ARROTONDA_MEZZO_PARI = _ott(_orig, 'ROUND_HALF_EVEN')
ARROTONDA_GIU = _ott(_orig, 'ROUND_DOWN')
ARROTONDA_SU = _ott(_orig, 'ROUND_UP')
ARROTONDA_VERSO_BASSO = _ott(_orig, 'ROUND_FLOOR')
ARROTONDA_VERSO_ALTO = _ott(_orig, 'ROUND_CEILING')
OperazioneNonValida = _ott(_orig, 'InvalidOperation')
DivisionePerZeroDecimale = _ott(_orig, 'DivisionByZero')
alias_tipo(_ott(_orig, 'Decimal'), {'quantizza': 'quantize', 'normalizza': 'normalize', 'come_tupla': 'as_tuple', 'è_nan': 'is_nan', 'è_finito': 'is_finite', 'aggiusta': 'adjusted'})
alias_tipo(_ott(_orig, 'Context'), {'precisione': 'prec', 'arrotondamento': 'rounding'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'base_contesto': 'BasicContext', 'contesto_predefinito': 'DefaultContext', 'esteso_contesto': 'ExtendedContext', 'HA_FILI': 'HAVE_THREADS', 'ARROTONDA_05_SU': 'ROUND_05UP'}
_AUTO_TIPI = {'Context': {'aggiungi': 'add', 'canonico': 'canonical', 'svuota_bandiere': 'clear_flags', 'confronta': 'compare', 'confronta_segnale': 'compare_signal', 'confronta_totale': 'compare_total', 'copia': 'copy', 'copia_decimale': 'copy_decimal', 'copia_firma': 'copy_sign', 'crea_decimale': 'create_decimal', 'crea_decimale_da_decimale': 'create_decimal_from_float', 'dividi': 'divide', 'dividi_intero': 'divide_int', 'esponenziale': 'exp', 'è_canonico': 'is_canonical', 'è_non_numero': 'is_nan', 'è_normale': 'is_normal', 'è_con_segno': 'is_signed', 'è_zero': 'is_zero', 'logico_e': 'logical_and', 'logico_inverti': 'logical_invert', 'logico_o': 'logical_or', 'logico_xor_': 'logical_xor', 'massimo': 'max', 'minimo': 'min', 'meno': 'minus', 'moltiplica': 'multiply', 'successivo_meno': 'next_minus', 'normalizza': 'normalize', 'numero_classe': 'number_class', 'potenza': 'power', 'quantizza': 'quantize', 'resto': 'remainder', 'ruota': 'rotate', 'sottrai': 'subtract', 'in_integrale': 'to_integral', 'in_integrale_esatto': 'to_integral_exact', 'in_integrale_valore': 'to_integral_value'}, 'Decimal': {'come_intero_rapporto': 'as_integer_ratio', 'come_tupla': 'as_tuple', 'canonico': 'canonical', 'confronta': 'compare', 'confronta_segnale': 'compare_signal', 'confronta_totale': 'compare_total', 'coniugato': 'conjugate', 'copia_firma': 'copy_sign', 'esponenziale': 'exp', 'da_decimale': 'from_float', 'immaginario': 'imag', 'è_canonico': 'is_canonical', 'è_non_numero': 'is_nan', 'è_normale': 'is_normal', 'è_con_segno': 'is_signed', 'è_zero': 'is_zero', 'logico_e': 'logical_and', 'logico_inverti': 'logical_invert', 'logico_o': 'logical_or', 'logico_xor_': 'logical_xor', 'massimo': 'max', 'minimo': 'min', 'successivo_meno': 'next_minus', 'normalizza': 'normalize', 'numero_classe': 'number_class', 'quantizza': 'quantize', 'reale': 'real', 'ruota': 'rotate', 'in_integrale': 'to_integral', 'in_integrale_esatto': 'to_integral_exact', 'in_integrale_valore': 'to_integral_value'}, 'DecimalTuple': {'cifre': 'digits', 'firma': 'sign'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
