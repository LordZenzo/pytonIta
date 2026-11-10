"""Modulo italiano per `shutil` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import shutil as _orig
from shutil import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

copia = _ott(_orig, 'copy')
copia_con_metadati = _ott(_orig, 'copy2')
copia_contenuto = _ott(_orig, 'copyfileobj')
copia_file = _ott(_orig, 'copyfile')
copia_albero = _ott(_orig, 'copytree')
sposta = _ott(_orig, 'move')
elimina_albero = _ott(_orig, 'rmtree')
spazio_disco = _ott(_orig, 'disk_usage')
cerca_programma = _ott(_orig, 'which')
crea_archivio = _ott(_orig, 'make_archive')
estrai_archivio = _ott(_orig, 'unpack_archive')
dimensione_terminale = _ott(_orig, 'get_terminal_size')
copia_permessi = _ott(_orig, 'copymode')
copia_statistiche = _ott(_orig, 'copystat')
ErroreOperazioniFile = _ott(_orig, 'Error')
ignora_modelli = _ott(_orig, 'ignore_patterns')
cambia_proprietario = _ott(_orig, 'chown')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'ottieni_spacchetta_formati': 'get_unpack_formats', 'registra_spacchetta_formato': 'register_unpack_format', 'annulla_registrazione_spacchetta_formato': 'unregister_unpack_format'}
_AUTO_TIPI = {}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
