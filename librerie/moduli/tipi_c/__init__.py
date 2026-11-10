"""Modulo italiano per `ctypes` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import ctypes as _orig
from ctypes import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

dll_windows = _ott(_orig, 'windll')
dll_c = _ott(_orig, 'cdll')
LibreriaC = _ott(_orig, 'CDLL')
LibreriaWindows = _ott(_orig, 'WinDLL')
intero_c = _ott(_orig, 'c_int')
intero_senza_segno_c = _ott(_orig, 'c_uint')
lungo_c = _ott(_orig, 'c_long')
lungo_senza_segno_c = _ott(_orig, 'c_ulong')
corto_c = _ott(_orig, 'c_short')
corto_senza_segno_c = _ott(_orig, 'c_ushort')
byte_c = _ott(_orig, 'c_byte')
byte_senza_segno_c = _ott(_orig, 'c_ubyte')
carattere_c = _ott(_orig, 'c_char')
carattere_largo_c = _ott(_orig, 'c_wchar')
puntatore_testo_c = _ott(_orig, 'c_char_p')
puntatore_testo_largo_c = _ott(_orig, 'c_wchar_p')
puntatore_vuoto = _ott(_orig, 'c_void_p')
decimale_c = _ott(_orig, 'c_float')
doppio_c = _ott(_orig, 'c_double')
booleano_c = _ott(_orig, 'c_bool')
dimensione_c = _ott(_orig, 'c_size_t')
intero64_c = _ott(_orig, 'c_int64')
intero64_senza_segno_c = _ott(_orig, 'c_uint64')
intero32_c = _ott(_orig, 'c_int32')
intero32_senza_segno_c = _ott(_orig, 'c_uint32')
intero16_c = _ott(_orig, 'c_int16')
intero16_senza_segno_c = _ott(_orig, 'c_uint16')
intero8_c = _ott(_orig, 'c_int8')
intero8_senza_segno_c = _ott(_orig, 'c_uint8')
Struttura = _ott(_orig, 'Structure')
Unione = _ott(_orig, 'Union')
PUNTATORE = _ott(_orig, 'POINTER')
puntatore = _ott(_orig, 'pointer')
per_riferimento = _ott(_orig, 'byref')
dimensione_di = _ott(_orig, 'sizeof')
converti = _ott(_orig, 'cast')
crea_buffer_testo = _ott(_orig, 'create_string_buffer')
crea_buffer_unicode = _ott(_orig, 'create_unicode_buffer')
indirizzo_di = _ott(_orig, 'addressof')
sposta_memoria = _ott(_orig, 'memmove')
imposta_memoria = _ott(_orig, 'memset')
testo_a = _ott(_orig, 'string_at')
testo_largo_a = _ott(_orig, 'wstring_at')
TIPO_FUNZIONE_C = _ott(_orig, 'CFUNCTYPE')
TIPO_FUNZIONE_WINDOWS = _ott(_orig, 'WINFUNCTYPE')
ErroreArgomento = _ott(_orig, 'ArgumentError')
ultimo_errore = _ott(_orig, 'get_last_error')
imposta_ultimo_errore = _ott(_orig, 'set_last_error')
ErroreWindows = _ott(_orig, 'WinError')
formatta_errore = _ott(_orig, 'FormatError')
ottieni_ultimo_errore = _ott(_orig, 'GetLastError')
Array = _ott(_orig, 'Array')
dimensione_con_segno_c = _ott(_orig, 'c_ssize_t')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'MODALITA_PREDEFINITO': 'DEFAULT_MODE', 'allineamento': 'alignment', 'ridimensiona': 'resize'}
_AUTO_TIPI = {'LibraryLoader': {'carica_libreria': 'LoadLibrary'}, 'c_char_p': {'da_parametro': 'from_param'}, 'c_void_p': {'da_parametro': 'from_param'}, 'c_voidp': {'da_parametro': 'from_param'}, 'c_wchar_p': {'da_parametro': 'from_param'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
