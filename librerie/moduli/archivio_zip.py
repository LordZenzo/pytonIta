"""Modulo italiano per `zipfile` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import zipfile as _orig
from zipfile import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

ArchivioZip = _ott(_orig, 'ZipFile')
InfoZip = _ott(_orig, 'ZipInfo')
COMPRESSO = _ott(_orig, 'ZIP_DEFLATED')
NON_COMPRESSO = _ott(_orig, 'ZIP_STORED')
è_zip = _ott(_orig, 'is_zipfile')
ZipNonValido = _ott(_orig, 'BadZipFile')
alias_tipo(_ott(_orig, 'ZipFile'), {'estrai_tutto': 'extractall', 'estrai': 'extract', 'elenco_nomi': 'namelist', 'elenco_info': 'infolist', 'scrivi': 'write', 'scrivi_testo': 'writestr', 'leggi': 'read', 'apri': 'open', 'chiudi': 'close', 'testa': 'testzip', 'ottieni_info': 'getinfo'})
alias_tipo(_ott(_orig, 'ZipInfo'), {'nome_file': 'filename', 'dimensione_file': 'file_size', 'dimensione_compressa': 'compress_size'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'CompleteDirs': {'crea': 'make'}, 'LZMACompressor': {'comprimi': 'compress', 'svuota_buffer': 'flush'}, 'LZMADecompressor': {'decomprimi': 'decompress'}, 'Path': {'esiste': 'exists', 'nome_file': 'filename', 'cerca': 'glob', 'è_cartella': 'is_dir', 'è_file': 'is_file', 'è_collegamento_simbolico': 'is_symlink', 'corrisponde': 'match', 'nome': 'name', 'apri': 'open', 'genitore': 'parent', 'leggi_byte': 'read_bytes', 'leggi_testo': 'read_text', 'fino_a_relativo': 'relative_to', 'cerca_ricorsivo': 'rglob', 'nome_senza_estensione': 'stem', 'suffisso': 'suffix', 'suffissi': 'suffixes'}, 'ZipExtFile': {'POSIZIONA_MASSIMO_LEGGI': 'MAX_SEEK_READ', 'LEGGI_MINIMO_DIMENSIONE': 'MIN_READ_SIZE', 'chiudi': 'close', 'sbircia': 'peek', 'leggi': 'read', 'leggibile': 'readable', 'leggi_riga': 'readline', 'posiziona': 'seek', 'posizionabile': 'seekable', 'posizione': 'tell'}, 'ZipFile': {'chiudi': 'close', 'commento': 'comment', 'estrai': 'extract', 'crea_cartella': 'mkdir', 'apri': 'open', 'leggi': 'read', 'scrivi': 'write'}, 'ZipInfo': {'file_intestazione': 'FileHeader', 'commento': 'comment', 'comprimi_livello': 'compress_level', 'comprimi_dimensione': 'compress_size', 'comprimi_tipo': 'compress_type', 'crea_sistema': 'create_system', 'crea_versione': 'create_version', 'data_tempo': 'date_time', 'attributo_esterno': 'external_attr', 'estrai_versione': 'extract_version', 'file_dimensione': 'file_size', 'nome_file': 'filename', 'bandiera_bit': 'flag_bits', 'da_file': 'from_file', 'intestazione_scostamento': 'header_offset', 'attributo_interno': 'internal_attr', 'è_cartella': 'is_dir', 'originale_nome_file': 'orig_filename', 'riservato': 'reserved'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
