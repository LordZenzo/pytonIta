"""Modulo italiano per `pathlib` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import pathlib as _orig
from pathlib import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

Percorso = _ott(_orig, 'Path')
PercorsoPuro = _ott(_orig, 'PurePath')
PercorsoWindows = _ott(_orig, 'WindowsPath')
alias_tipo(_ott(_orig, 'PurePath'), {'nome': 'name', 'suffisso': 'suffix', 'suffissi': 'suffixes', 'nome_senza_estensione': 'stem', 'genitore': 'parent', 'genitori': 'parents', 'parti': 'parts', 'unità': 'drive', 'radice': 'root', 'è_assoluto': 'is_absolute', 'unisci_percorso': 'joinpath', 'con_nome': 'with_name', 'con_suffisso': 'with_suffix', 'con_nome_senza_estensione': 'with_stem', 'relativo_a': 'relative_to', 'è_relativo_a': 'is_relative_to', 'in_posix': 'as_posix', 'corrisponde': 'match'})
alias_tipo(_ott(_orig, 'Path'), {'esiste': 'exists', 'è_file': 'is_file', 'è_cartella': 'is_dir', 'crea_cartella': 'mkdir', 'leggi_testo': 'read_text', 'scrivi_testo': 'write_text', 'leggi_byte': 'read_bytes', 'scrivi_byte': 'write_bytes', 'apri': 'open', 'elimina_file': 'unlink', 'rimuovi_cartella': 'rmdir', 'rinomina': 'rename', 'sostituisci': 'replace', 'elenca': 'iterdir', 'cerca': 'glob', 'cerca_ricorsivo': 'rglob', 'statistiche': 'stat', 'risolvi': 'resolve', 'assoluto': 'absolute', 'espandi_utente': 'expanduser', 'casa': 'home', 'cartella_corrente': 'cwd', 'tocca': 'touch', 'è_collegamento': 'is_symlink', 'proprietario': 'owner', 'visita': 'walk'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'Path': {'assoluto': 'absolute', 'come_uri': 'as_uri', 'cambia_permessi': 'chmod', 'da_uri': 'from_uri', 'cerca': 'glob', 'crea_cartella': 'mkdir', 'apri': 'open', 'leggi_testo': 'read_text', 'rinomina': 'rename', 'sostituisci': 'replace', 'cerca_ricorsivo': 'rglob', 'rimuovi_cartella': 'rmdir', 'statistiche': 'stat', 'collegamento_simbolico_fino_a': 'symlink_to', 'tocca': 'touch', 'scollega': 'unlink', 'visita': 'walk', 'scrivi_testo': 'write_text'}, 'PurePath': {'ancora': 'anchor', 'come_uri': 'as_uri', 'unita': 'drive', 'è_assoluto': 'is_absolute', 'è_fino_a_relativo': 'is_relative_to', 'è_riservato': 'is_reserved', 'nome': 'name', 'genitore': 'parent', 'genitori': 'parents', 'analizzatore': 'parser', 'parti': 'parts', 'fino_a_relativo': 'relative_to', 'radice': 'root', 'con_nome': 'with_name'}, 'PurePosixPath': {'analizzatore': 'parser'}, 'PureWindowsPath': {'analizzatore': 'parser'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
