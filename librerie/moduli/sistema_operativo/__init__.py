"""Modulo italiano per `os` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import os as _orig
from os import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

cartella_corrente = _ott(_orig, 'getcwd')
cambia_cartella = _ott(_orig, 'chdir')
elenco_cartelle = _ott(_orig, 'listdir')
crea_cartella = _ott(_orig, 'mkdir')
crea_cartelle = _ott(_orig, 'makedirs')
rimuovi_file = _ott(_orig, 'remove')
rimuovi_cartella = _ott(_orig, 'rmdir')
rimuovi_cartelle = _ott(_orig, 'removedirs')
rinomina = _ott(_orig, 'rename')
sostituisci = _ott(_orig, 'replace')
ambiente = _ott(_orig, 'environ')
ottieni_ambiente = _ott(_orig, 'getenv')
imposta_ambiente = _ott(_orig, 'putenv')
separatore = _ott(_orig, 'sep')
separatore_percorsi = _ott(_orig, 'pathsep')
fine_riga = _ott(_orig, 'linesep')
nome_sistema = _ott(_orig, 'name')
esegui_comando = _ott(_orig, 'system')
scansiona = _ott(_orig, 'scandir')
visita = _ott(_orig, 'walk')
avvia_file = _ott(_orig, 'startfile')
ottieni_pid = _ott(_orig, 'getpid')
termina_processo = _ott(_orig, 'kill')
statistiche_file = _ott(_orig, 'stat')
conta_cpu = _ott(_orig, 'cpu_count')
dimensione_terminale = _ott(_orig, 'get_terminal_size')
file_nullo = _ott(_orig, 'devnull')
ottieni_utente = _ott(_orig, 'getlogin')
apri_descrittore = _ott(_orig, 'open')

from . import percorso
alias_tipo(_orig.DirEntry, {'nome': 'name', 'percorso_completo': 'path',
    'è_file': 'is_file', 'è_cartella': 'is_dir', 'è_collegamento': 'is_symlink',
    'statistiche': 'stat'})
alias_tipo(type(_orig.stat('.')), {'dimensione': 'st_size', 'modifica_tempo': 'st_mtime',
    'creazione_tempo': 'st_ctime', 'accesso_tempo': 'st_atime', 'modalita': 'st_mode'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'POSIZIONA_FINE': 'SEEK_END', 'POSIZIONA_INSIEME': 'SEEK_SET', 'TEMPORANEO_MASSIMO': 'TMP_MAX', 'accesso': 'access', 'cambia_permessi': 'chmod', 'chiudi': 'close', 'dispositivo_codifica': 'device_encoding', 'duplica': 'dup', 'ottieni_bloccante': 'get_blocking', 'ottieni_esegui_percorso': 'get_exec_path', 'ottieni_gestisci_ereditabile': 'get_handle_inheritable', 'ottieni_ereditabile': 'get_inheritable', 'collega': 'link', 'leggi': 'read', 'imposta_bloccante': 'set_blocking', 'imposta_gestisci_ereditabile': 'set_handle_inheritable', 'imposta_ereditabile': 'set_inheritable', 'collegamento_simbolico': 'symlink', 'tronca': 'truncate', 'scollega': 'unlink', 'scrivi': 'write'}
_AUTO_TIPI = {'terminal_size': {'colonne': 'columns', 'linee': 'lines'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
