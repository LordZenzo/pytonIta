"""Modulo italiano per `tarfile` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import tarfile as _orig
from tarfile import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

apri = _ott(_orig, 'open')
ArchivioTar = _ott(_orig, 'TarFile')
InfoTar = _ott(_orig, 'TarInfo')
è_tar = _ott(_orig, 'is_tarfile')
ErroreTar = _ott(_orig, 'TarError')
alias_tipo(_ott(_orig, 'TarFile'), {'aggiungi': 'add', 'estrai_tutto': 'extractall', 'estrai': 'extract', 'elenco_nomi': 'getnames', 'elenco_membri': 'getmembers', 'ottieni_membro': 'getmember', 'chiudi': 'close', 'elenca': 'list'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'FORMATO_PREDEFINITO': 'DEFAULT_FORMAT', 'CODIFICA': 'ENCODING', 'dati_filtra': 'data_filter', 'tar_filtra': 'tar_filter'}
_AUTO_TIPI = {'TarFile': {'aggiungi': 'add', 'cambia_permessi': 'chmod', 'cambia_proprietario': 'chown', 'chiudi': 'close', 'codifica': 'encoding', 'errori': 'errors', 'estrai': 'extract', 'formatta': 'format', 'elenca': 'list', 'successivo': 'next'}, 'TarInfo': {'ottieni_informazione': 'get_info', 'modalita': 'mode', 'nome': 'name', 'scostamento': 'offset', 'scostamento_dati': 'offset_data', 'percorso': 'path', 'sostituisci': 'replace', 'dimensione': 'size', 'tipo': 'type'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
