"""Modulo italiano per `winreg` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import winreg as _orig
from winreg import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

apri_chiave = _ott(_orig, 'OpenKey')
crea_chiave = _ott(_orig, 'CreateKey')
chiudi_chiave = _ott(_orig, 'CloseKey')
leggi_valore = _ott(_orig, 'QueryValueEx')
scrivi_valore = _ott(_orig, 'SetValueEx')
elimina_valore = _ott(_orig, 'DeleteValue')
elimina_chiave = _ott(_orig, 'DeleteKey')
enumera_chiave = _ott(_orig, 'EnumKey')
enumera_valore = _ott(_orig, 'EnumValue')
CHIAVE_UTENTE_CORRENTE = _ott(_orig, 'HKEY_CURRENT_USER')
CHIAVE_MACCHINA_LOCALE = _ott(_orig, 'HKEY_LOCAL_MACHINE')
CHIAVE_RADICE_CLASSI = _ott(_orig, 'HKEY_CLASSES_ROOT')
TESTO = _ott(_orig, 'REG_SZ')
INTERO_32 = _ott(_orig, 'REG_DWORD')
TESTO_ESPANDIBILE = _ott(_orig, 'REG_EXPAND_SZ')
ACCESSO_LETTURA = _ott(_orig, 'KEY_READ')
ACCESSO_SCRITTURA = _ott(_orig, 'KEY_WRITE')
ACCESSO_TUTTO = _ott(_orig, 'KEY_ALL_ACCESS')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'svuota_buffer_chiave': 'FlushKey', 'CHIAVE_CREA_COLLEGA': 'KEY_CREATE_LINK', 'CHIAVE_ESEGUI': 'KEY_EXECUTE', 'CHIAVE_NOTIFICA': 'KEY_NOTIFY', 'CHIAVE_INTERROGAZIONE_VALORE': 'KEY_QUERY_VALUE', 'CHIAVE_INSIEME_VALORE': 'KEY_SET_VALUE', 'carica_chiave': 'LoadKey', 'interrogazione_informazione_chiave': 'QueryInfoKey', 'interrogazione_valore': 'QueryValue', 'salva_chiave': 'SaveKey', 'imposta_valore': 'SetValue'}
_AUTO_TIPI = {'HKEYType': {'chiudi': 'Close', 'stacca': 'Detach', 'gestisci': 'handle'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
