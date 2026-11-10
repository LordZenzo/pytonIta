"""Modulo italiano per `inspect` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import inspect as _orig
from inspect import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

ottieni_membri = _ott(_orig, 'getmembers')
firma = _ott(_orig, 'signature')
è_funzione = _ott(_orig, 'isfunction')
è_classe = _ott(_orig, 'isclass')
è_metodo = _ott(_orig, 'ismethod')
è_modulo = _ott(_orig, 'ismodule')
ottieni_sorgente = _ott(_orig, 'getsource')
ottieni_documentazione = _ott(_orig, 'getdoc')
ottieni_file = _ott(_orig, 'getfile')
pila = _ott(_orig, 'stack')
frame_corrente = _ott(_orig, 'currentframe')
è_generatore = _ott(_orig, 'isgenerator')
è_coroutine = _ott(_orig, 'iscoroutine')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'GENERA_CHIUSO': 'GEN_CLOSED', 'GENERA_CREATO': 'GEN_CREATED', 'ottieni_annotazioni': 'get_annotations', 'traccia': 'trace', 'scarta_avvolgimento': 'unwrap'}
_AUTO_TIPI = {'ArgInfo': {'argomenti': 'args', 'parole_chiave': 'keywords', 'locali': 'locals', 'argomenti_variabili': 'varargs'}, 'Arguments': {'argomenti': 'args', 'argomenti_variabili': 'varargs'}, 'Attribute': {'genere': 'kind', 'nome': 'name', 'oggetto': 'object'}, 'BoundArguments': {'applica_predefiniti': 'apply_defaults', 'argomenti': 'args', 'argomenti_con_nome': 'kwargs'}, 'BufferFlags': {'QUALSIASI_CONTIGUO': 'ANY_CONTIGUOUS', 'FORMATTA': 'FORMAT', 'COMPLETO': 'FULL', 'LEGGI': 'READ', 'RECORD': 'RECORDS', 'SEMPLICE': 'SIMPLE', 'SCRIVIBILE': 'WRITABLE', 'SCRIVI': 'WRITE'}, 'ClosureVars': {'globali': 'globals'}, 'FullArgSpec': {'annotazioni': 'annotations', 'argomenti': 'args', 'predefiniti': 'defaults', 'argomenti_variabili': 'varargs'}, 'Parameter': {'PAROLA_CHIAVE_SOLO': 'KEYWORD_ONLY', 'POSIZIONALE_SOLO': 'POSITIONAL_ONLY', 'POSIZIONALE_O_PAROLA_CHIAVE': 'POSITIONAL_OR_KEYWORD', 'annotazione': 'annotation', 'predefinito': 'default', 'vuoto': 'empty', 'genere': 'kind', 'nome': 'name', 'sostituisci': 'replace'}, 'Signature': {'associa': 'bind', 'associa_parziale': 'bind_partial', 'vuoto': 'empty', 'formatta': 'format', 'parametri': 'parameters', 'sostituisci': 'replace'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
