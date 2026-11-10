"""Modulo italiano per `collections` (generato da tools/genera_moduli.py).

Contiene tutti i nomi originali piu' gli alias italiani.
"""
import collections as _orig
from collections import *
from _italiano import alias_tipo, kw_tipo, ottieni as _ott


def __getattr__(nome):
    return getattr(_orig, nome)

contatore = _ott(_orig, 'Counter')
dizionario_ordinato = _ott(_orig, 'OrderedDict')
dizionario_predefinito = _ott(_orig, 'defaultdict')
coda_doppia = _ott(_orig, 'deque')
tupla_con_nome = _ott(_orig, 'namedtuple')
mappa_concatenata = _ott(_orig, 'ChainMap')
alias_tipo(_ott(_orig, 'Counter'), {'elementi': 'elements', 'più_comuni': 'most_common', 'sottrai': 'subtract', 'totale': 'total'})
alias_tipo(_ott(_orig, 'deque'), {'aggiungi_a_destra': 'append', 'aggiungi_a_sinistra': 'appendleft', 'estrai_da_destra': 'pop', 'estrai_da_sinistra': 'popleft', 'ruota': 'rotate', 'estendi_a_sinistra': 'extendleft'})
alias_tipo(_ott(_orig, 'OrderedDict'), {'sposta_alla_fine': 'move_to_end'})

# --- traduzione automatica del resto dell'API (glossario) ---
_AUTO_NOMI = {}
_AUTO_TIPI = {'ChainMap': {'svuota': 'clear', 'copia': 'copy', 'da_chiavi': 'fromkeys', 'ottieni': 'get', 'nuovo_figlio': 'new_child', 'genitori': 'parents', 'estrai': 'pop'}, 'Counter': {'copia': 'copy', 'elementi': 'elements', 'da_chiavi': 'fromkeys', 'sottrai': 'subtract', 'totale': 'total', 'aggiorna': 'update'}, 'OrderedDict': {'svuota': 'clear', 'copia': 'copy', 'da_chiavi': 'fromkeys', 'elementi': 'items', 'chiavi': 'keys', 'sposta_in_fine': 'move_to_end', 'estrai': 'pop', 'aggiorna': 'update', 'valori': 'values'}, 'UserDict': {'copia': 'copy', 'da_chiavi': 'fromkeys', 'ottieni': 'get'}, 'UserList': {'aggiungi': 'append', 'svuota': 'clear', 'copia': 'copy', 'conta': 'count', 'estendi': 'extend', 'indice': 'index', 'inserisci': 'insert', 'estrai': 'pop', 'rimuovi': 'remove', 'inverti': 'reverse', 'ordina': 'sort'}, 'UserString': {'capitalizza': 'capitalize', 'centro': 'center', 'conta': 'count', 'codifica': 'encode', 'finisce_con': 'endswith', 'trova': 'find', 'formatta': 'format', 'formatta_mappa': 'format_map', 'indice': 'index', 'unisci': 'join', 'allinea_a_sinistra': 'ljust', 'porta_sotto': 'lower', 'elimina_spazi_sinistra': 'lstrip', 'sostituisci': 'replace', 'allinea_a_destra': 'rjust', 'elimina_spazi_destra': 'rstrip', 'separa': 'split', 'inizia_con': 'startswith', 'elimina_spazi': 'strip', 'inverti_maiuscole': 'swapcase', 'titolo': 'title', 'trasla': 'translate', 'maiuscolo': 'upper', 'riempi_zeri': 'zfill'}, 'defaultdict': {'copia': 'copy', 'fabbrica_predefinito': 'default_factory'}, 'deque': {'aggiungi': 'append', 'svuota': 'clear', 'copia': 'copy', 'conta': 'count', 'estendi': 'extend', 'indice': 'index', 'inserisci': 'insert', 'estrai': 'pop', 'rimuovi': 'remove', 'inverti': 'reverse', 'ruota': 'rotate'}}
from _italiano import applica_auto as _auto
_auto(globals(), _orig, _AUTO_NOMI, _AUTO_TIPI)

from _italiano import importa_basi as _basi
_basi(_orig)
