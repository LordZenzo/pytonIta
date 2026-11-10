"""Modulo italiano per `ctypes.wintypes` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import ctypes.wintypes as _orig
from ctypes.wintypes import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

MANIGLIA = _ott(_orig, 'HANDLE')
FINESTRA = _ott(_orig, 'HWND')
PAROLA = _ott(_orig, 'WORD')
DOPPIA_PAROLA = _ott(_orig, 'DWORD')
BOOLEANO = _ott(_orig, 'BOOL')
PUNTO = _ott(_orig, 'POINT')
RETTANGOLO = _ott(_orig, 'RECT')
LPARAM = _ott(_orig, 'LPARAM')
WPARAM = _ott(_orig, 'WPARAM')
ISTANZA = _ott(_orig, 'HINSTANCE')
MODULO = _ott(_orig, 'HMODULE')
MENU = _ott(_orig, 'HMENU')
ICONA = _ott(_orig, 'HICON')
PENNELLO = _ott(_orig, 'HBRUSH')
CONTESTO_DISPOSITIVO = _ott(_orig, 'HDC')
COSTANTE_TESTO = _ott(_orig, 'LPCWSTR')
COSTANTE_TESTO_C = _ott(_orig, 'LPCSTR')
LUNGO = _ott(_orig, 'LONG')
MESSAGGIO = _ott(_orig, 'MSG')
DIMENSIONE = _ott(_orig, 'SIZE')
INTERO_SENZA_SEGNO = _ott(_orig, 'UINT')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'CARATTERE': 'CHAR', 'DOPPIO': 'DOUBLE', 'DECIMALE': 'FLOAT', 'INTERO': 'INT', 'GRANDE_INTERO': 'LARGE_INTEGER', 'PERCORSO_MASSIMO': 'MAX_PATH', 'SERVIZIO_STATO_GESTISCI': 'SERVICE_STATUS_HANDLE', 'CORTO': 'SHORT', 'VARIANTE_BOOLEANO': 'VARIANT_BOOL'}
_AUTO_TIPI = {'HACCEL': {'da_parametro': 'from_param'}, 'HANDLE': {'da_parametro': 'from_param'}, 'HBITMAP': {'da_parametro': 'from_param'}, 'HBRUSH': {'da_parametro': 'from_param'}, 'HCOLORSPACE': {'da_parametro': 'from_param'}, 'HDC': {'da_parametro': 'from_param'}, 'HDESK': {'da_parametro': 'from_param'}, 'HDWP': {'da_parametro': 'from_param'}, 'HENHMETAFILE': {'da_parametro': 'from_param'}, 'HFONT': {'da_parametro': 'from_param'}, 'HGDIOBJ': {'da_parametro': 'from_param'}, 'HGLOBAL': {'da_parametro': 'from_param'}, 'HHOOK': {'da_parametro': 'from_param'}, 'HICON': {'da_parametro': 'from_param'}, 'HINSTANCE': {'da_parametro': 'from_param'}, 'HKEY': {'da_parametro': 'from_param'}, 'HKL': {'da_parametro': 'from_param'}, 'HLOCAL': {'da_parametro': 'from_param'}, 'HMENU': {'da_parametro': 'from_param'}, 'HMETAFILE': {'da_parametro': 'from_param'}, 'HMODULE': {'da_parametro': 'from_param'}, 'HMONITOR': {'da_parametro': 'from_param'}, 'HPALETTE': {'da_parametro': 'from_param'}, 'HPEN': {'da_parametro': 'from_param'}, 'HRGN': {'da_parametro': 'from_param'}, 'HRSRC': {'da_parametro': 'from_param'}, 'HSTR': {'da_parametro': 'from_param'}, 'HTASK': {'da_parametro': 'from_param'}, 'HWINSTA': {'da_parametro': 'from_param'}, 'HWND': {'da_parametro': 'from_param'}, 'LPCOLESTR': {'da_parametro': 'from_param'}, 'LPCSTR': {'da_parametro': 'from_param'}, 'LPCVOID': {'da_parametro': 'from_param'}, 'LPCWSTR': {'da_parametro': 'from_param'}, 'LPOLESTR': {'da_parametro': 'from_param'}, 'LPSTR': {'da_parametro': 'from_param'}, 'LPVOID': {'da_parametro': 'from_param'}, 'LPWSTR': {'da_parametro': 'from_param'}, 'MSG': {'messaggio': 'message', 'tempo': 'time'}, 'OLESTR': {'da_parametro': 'from_param'}, 'PCHAR': {'da_parametro': 'from_param'}, 'PWCHAR': {'da_parametro': 'from_param'}, 'RECT': {'basso': 'bottom', 'sinistra': 'left', 'destra': 'right', 'alto': 'top'}, 'RECTL': {'basso': 'bottom', 'sinistra': 'left', 'destra': 'right', 'alto': 'top'}, 'SC_HANDLE': {'da_parametro': 'from_param'}, 'SERVICE_STATUS_HANDLE': {'da_parametro': 'from_param'}, 'SMALL_RECT': {'basso': 'Bottom', 'sinistra': 'Left', 'destra': 'Right', 'alto': 'Top'}, 'tagMSG': {'messaggio': 'message', 'tempo': 'time'}, 'tagRECT': {'basso': 'bottom', 'sinistra': 'left', 'destra': 'right', 'alto': 'top'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
