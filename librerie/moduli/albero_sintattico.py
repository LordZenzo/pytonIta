"""Modulo italiano per `ast` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import ast as _orig
from ast import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

analizza = _ott(_orig, 'parse')
scarica = _ott(_orig, 'dump')
valuta_letterale = _ott(_orig, 'literal_eval')
visita = _ott(_orig, 'walk')
VisitatoreNodi = _ott(_orig, 'NodeVisitor')
TrasformatoreNodi = _ott(_orig, 'NodeTransformer')
Nodo = _ott(_orig, 'AST')
ripara_posizioni = _ott(_orig, 'fix_missing_locations')
copia_posizione = _ott(_orig, 'copy_location')
ottieni_docstring = _ott(_orig, 'get_docstring')
ottieni_sorgente = _ott(_orig, 'get_source_segment')
annulla_analisi = _ott(_orig, 'unparse')

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {'itera_figlio_nodi': 'iter_child_nodes', 'itera_campi': 'iter_fields', 'principale': 'main'}
_AUTO_TIPI = {'AnnAssign': {'valore': 'value'}, 'Assert': {'messaggio': 'msg'}, 'Assign': {'tipo_commento': 'type_comment'}, 'AsyncFor': {'tipo_commento': 'type_comment'}, 'AsyncFunctionDef': {'tipo_commento': 'type_comment'}, 'AsyncWith': {'tipo_commento': 'type_comment'}, 'Constant': {'genere': 'kind'}, 'ExceptHandler': {'nome': 'name', 'tipo': 'type'}, 'For': {'tipo_commento': 'type_comment'}, 'FunctionDef': {'tipo_commento': 'type_comment'}, 'ImportFrom': {'livello': 'level', 'modulo': 'module'}, 'MatchAs': {'nome': 'name', 'modello': 'pattern'}, 'MatchStar': {'nome': 'name'}, 'ParamSpec': {'valore_predefinito': 'default_value'}, 'Raise': {'causa': 'cause', 'eccezione': 'exc'}, 'Return': {'valore': 'value'}, 'Slice': {'porta_sotto': 'lower', 'passo': 'step', 'maiuscolo': 'upper'}, 'TypeVar': {'valore_predefinito': 'default_value'}, 'TypeVarTuple': {'valore_predefinito': 'default_value'}, 'With': {'tipo_commento': 'type_comment'}, 'Yield': {'valore': 'value'}, 'alias': {'fine_colonna_scostamento': 'end_col_offset'}, 'arg': {'annotazione': 'annotation', 'fine_colonna_scostamento': 'end_col_offset', 'tipo_commento': 'type_comment'}, 'excepthandler': {'fine_colonna_scostamento': 'end_col_offset'}, 'expr': {'fine_colonna_scostamento': 'end_col_offset'}, 'keyword': {'fine_colonna_scostamento': 'end_col_offset'}, 'stmt': {'fine_colonna_scostamento': 'end_col_offset'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
