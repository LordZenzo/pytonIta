"""Modulo italiano per `typing` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import typing as _orig
from typing import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

Lista = _ott(_orig, 'List')
Dizionario = _ott(_orig, 'Dict')
Opzionale = _ott(_orig, 'Optional')
Unione = _ott(_orig, 'Union')
Qualsiasi = _ott(_orig, 'Any')
Richiamabile = _ott(_orig, 'Callable')
Tupla = _ott(_orig, 'Tuple')
Insieme = _ott(_orig, 'Set')
Iterabile = _ott(_orig, 'Iterable')
Iteratore = _ott(_orig, 'Iterator')
Sequenza = _ott(_orig, 'Sequence')
Mappatura = _ott(_orig, 'Mapping')
VariabileDiTipo = _ott(_orig, 'TypeVar')
Generico = _ott(_orig, 'Generic')
Protocollo = _ott(_orig, 'Protocol')
TuplaConNome = _ott(_orig, 'NamedTuple')
DizionarioTipizzato = _ott(_orig, 'TypedDict')
Letterale = _ott(_orig, 'Literal')
Finale = _ott(_orig, 'Final')
VariabileDiClasse = _ott(_orig, 'ClassVar')
converti_tipo = _ott(_orig, 'cast')
CONTROLLO_TIPI = _ott(_orig, 'TYPE_CHECKING')
SeStesso = _ott(_orig, 'Self')
Annotato = _ott(_orig, 'Annotated')
ottieni_suggerimenti_tipo = _ott(_orig, 'get_type_hints')
sovraccarico = _ott(_orig, 'overload')
NessunRitorno = _ott(_orig, 'NoReturn')
Generatore = _ott(_orig, 'Generator')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'qualsiasi_testo': 'AnyStr', 'contesto_asincrono_gestore': 'AsyncContextManager', 'generatore_asincrono': 'AsyncGenerator', 'iterabile_asincrono': 'AsyncIterable', 'byte_stringa': 'ByteString', 'collezione': 'Collection', 'contesto_gestore': 'ContextManager', 'coroutine': 'Coroutine', 'contatore': 'Counter', 'dizionario_predefinito': 'DefaultDict', 'elementi_vista': 'ItemsView', 'chiavi_vista': 'KeysView', 'letterale_stringa': 'LiteralString', 'mappatura_vista': 'MappingView', 'corrisponde': 'Match', 'nessun_predefinito': 'NoDefault', 'non_obbligatorio': 'NotRequired', 'dizionario_ordinato': 'OrderedDict', 'modello': 'Pattern', 'leggi_solo': 'ReadOnly', 'obbligatorio': 'Required', 'tipo': 'Type', 'tipo_è': 'TypeIs', 'spacchetta': 'Unpack', 'valori_vista': 'ValuesView', 'ottieni_argomenti': 'get_args', 'ottieni_origine': 'get_origin', 'ottieni_protocollo_membri': 'get_protocol_members', 'è_protocollo': 'is_protocol', 'nessun_tipo_controlla': 'no_type_check'}
_AUTO_TIPI = {'BinaryIO': {'scrivi': 'write'}, 'IO': {'chiudi': 'close', 'chiuso': 'closed', 'descrittore': 'fileno', 'svuota_buffer': 'flush', 'modalita': 'mode', 'nome': 'name', 'leggi': 'read', 'leggibile': 'readable', 'leggi_riga': 'readline', 'posiziona': 'seek', 'posizionabile': 'seekable', 'posizione': 'tell', 'tronca': 'truncate', 'scrivibile': 'writable', 'scrivi': 'write'}, 'ParamSpec': {'argomenti': 'args', 'ha_predefinito': 'has_default', 'argomenti_con_nome': 'kwargs'}, 'TextIO': {'codifica': 'encoding', 'errori': 'errors'}, 'TypeVar': {'ha_predefinito': 'has_default'}, 'TypeVarTuple': {'ha_predefinito': 'has_default'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
